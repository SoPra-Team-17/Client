"""
Implements the actual playing field
"""
import logging
import cppyy

from view.BasicView import BasicView
from view.GameView.Drawable import *
from view.GameView.Camera import Camera
from view.GameView.AssetStorage import AssetStorage
from view.ViewSettings import ViewSettings
from util.Coordinates import WorldPoint
from util.Datastructures import DrawableMap
from network.NetworkEvent import NETWORK_EVENT

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("datatypes/gadgets/GadgetEnum.hpp")


class PlayingFieldScreen(BasicView):
    """
    This class contains all the relevant information for drawing the playing field
    """

    def __init__(self, window: pygame.display, controller, parent_view, settings: ViewSettings):
        super(PlayingFieldScreen, self).__init__(window, controller, settings)

        self.parent_view = parent_view

        self.asset_storage = AssetStorage()
        self.camera = self.camera = Camera(camera_speed=.5)

        self.background_image = pygame.image.load("assets/GameView/background.png")
        self.background_image = pygame.transform.scale(self.background_image, (1920, 1080))

        self.request_operation = False

        self.map = FieldMap(settings)

    def draw(self):
        self.camera.move_camera(pygame.key.get_pressed())
        self.window.blit(self.background_image, (0, 0))
        self.map.highlight_drawable_in_focus(self.camera.getTrans())
        self.map.draw(self.window, self.camera.getTrans())

    def receive_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.camera.center()

        if event.type == pygame.MOUSEBUTTONUP:
            self.map.select_block(self.camera.getTrans())

        if event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT:
            if event.message_type == "GameStatus":
                self.update_playingfield()
            elif event.message_type == "RequestGameOperation":
                self._update_active_character()

    def update_playingfield(self) -> None:
        """
        This method is called when a updated playing field is received over the network (Game Status message)
        :return:    None
        """
        state = self.controller.lib_client_handler.lib_client.getState()
        field_map = state.getMap()

        n_rows = field_map.getNumberOfRows()

        # todo expect rectangle shaped playing field
        self.map.x_max = n_rows
        self.map.y_max = field_map.getRowLength(0)

        # old map is discarded
        self.map.map = DrawableMap((self.map.x_max, self.map.y_max, 3))

        for x in range(n_rows):
            for y in range(field_map.getRowLength(x)):
                self.map.map[WorldPoint(x, y, z=0)] = Floor(WorldPoint(x, y, z=0), self.asset_storage)

                field = field_map.getField(x, y)

                field_state = field.getFieldState()
                switcher = {
                    cppyy.gbl.spy.scenario.FieldStateEnum.BAR_TABLE: BarTable,
                    cppyy.gbl.spy.scenario.FieldStateEnum.ROULETTE_TABLE: RouletteTable,
                    cppyy.gbl.spy.scenario.FieldStateEnum.WALL: Wall,
                    cppyy.gbl.spy.scenario.FieldStateEnum.FREE: None,
                    cppyy.gbl.spy.scenario.FieldStateEnum.BAR_SEAT: BarSeat,
                    cppyy.gbl.spy.scenario.FieldStateEnum.SAFE: Safe,
                    cppyy.gbl.spy.scenario.FieldStateEnum.FIREPLACE: Fireplace
                }
                try:
                    if field_state is not None:
                        self.map.map[WorldPoint(x, y, z=1)] = switcher.get(field_state)(WorldPoint(x, y, z=1),
                                                                                        self.asset_storage)
                except TypeError:
                    pass

                # check if field has gadget
                if field.getGadget().has_value():
                    if field.getGadget().value().getType() == cppyy.gbl.spy.gadget.GadgetEnum.COCKTAIL:
                        self.map.map[WorldPoint(x, y, z=2)] = Cocktail(WorldPoint(x, y, z=2), self.asset_storage)
                    else:
                        self.map.map[WorldPoint(x, y, z=1)] = Gadget(WorldPoint(x, y, z=1), self.asset_storage)

                # check if field is foggy
                if field.isFoggy():
                    self.map.map[WorldPoint(x, y, z=1)] = Fog(WorldPoint(x, y, z=1), self.asset_storage)

        # add characters
        for char in state.getCharacters():
            if not char.getCoordinates().has_value():
                continue

            type = "invalid"

            chosen_chars = self.controller.lib_client_handler.lib_client.getMyFactionList()
            for chosen_chard_id in chosen_chars:
                if chosen_chard_id == char.getCharacterId():
                    type = "my"

            npc_chars = self.controller.lib_client_handler.lib_client.getNpcFactionList()
            for npc_char_id in npc_chars:
                if npc_char_id == char.getCharacterId():
                    type = "npc"

            enemy_chars = self.controller.lib_client_handler.lib_client.getEnemyFactionList()
            for enemy_char_id in enemy_chars:
                if enemy_char_id == char.getCharacterId():
                    type = "enemy"

            point = char.getCoordinates().value()
            self.map.map[WorldPoint(point.x, point.y, z=1)] = Character(WorldPoint(point.x, point.y, z=1),
                                                                        self.asset_storage, d_type=type)
        # check if janitor is on playing field
        if state.getJanitorCoordinates().has_value():
            pos_cpp = state.getJanitorCoordinates().value()
            self.map.map[WorldPoint(pos_cpp.x, pos_cpp.y, z=1)] = Character(WorldPoint(pos_cpp.x, pos_cpp.y, z=1),
                                                                            self.asset_storage, d_type="janitor")

        # check if cat is on playing field
        if state.getCatCoordinates().has_value():
            pos_cpp = state.getCatCoordinates().value()
            self.map.map[WorldPoint(pos_cpp.x, pos_cpp.y, z=1)] = Cat(WorldPoint(pos_cpp.x, pos_cpp.y, z=1),
                                                                      self.asset_storage)

        logging.info("Successfully updated playing field")

    def _update_active_character(self):
        active_char_id = self.controller.lib_client_handler.lib_client.getActiveCharacter()
        active_char = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
            active_char_id)
        if active_char.getCoordinates().has_value():
            active_char_coords = active_char.getCoordinates().value()
            wp_coords = WorldPoint(active_char_coords.x, active_char_coords.y, z=1)
            self.map.map[wp_coords] = Character(wp_coords, self.asset_storage, d_type="my", active=True)
