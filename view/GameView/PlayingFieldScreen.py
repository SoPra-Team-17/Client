"""
Implements the actual playing field
"""
import logging
import pygame
import cppyy

from view.BasicView import BasicView
from view.GameView.Drawable import *
from view.GameView.Camera import Camera
from view.GameView.AssetStorage import AssetStorage
from view.ViewSettings import ViewSettings
from util.Transforms import Transformations
from util.Coordinates import WorldPoint
from util.Datastructures import DrawableMap
from network.NetworkEvent import NETWORK_EVENT, NETWORK_EVENT_MESSAGE_TYPES

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"


class PlayingFieldScreen(BasicView):
    """
    This class contains all the relevant information for drawing the playing field
    """

    def __init__(self, window: pygame.display, controller, parent_view, settings: ViewSettings):
        super(PlayingFieldScreen, self).__init__(window, controller, settings)

        self.parent_view = parent_view

        self.asset_storage = AssetStorage()
        self.camera = self.camera = Camera(camera_speed=.5)

        # todo values are hardcoded, do in update_playingfield, when executed for the first time
        map = DrawableMap((50, 50, 3))

        self.background_image = pygame.image.load("assets/GameView/background.png")
        self.background_image = pygame.transform.scale(self.background_image, (1920, 1080))

        self.map = FieldMap(settings)
        self.map.map = map

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
            # todo remove debug info
            pos = pygame.mouse.get_pos()
            offsetX, offsetY = self.camera.getTrans()
            xTrans, yTrans = Transformations.trafo_window_to_world_coords(pos[0], pos[1], offsetX, offsetY)
            print(f"PosX: {xTrans}\tPosY: {yTrans}")

            self.map.select_block(self.camera.getTrans())

        if event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT:
            if event.message_type == "GameStatus":
                self.update_playingfield()

    def update_playingfield(self) -> None:
        """
        This method is called when a updated playing field is received over the network (Game Status message)
        :return:    None
        """
        # old map is discarded
        self.map.map = DrawableMap((50, 50, 3))

        state = self.controller.lib_client_handler.lib_client.getState()
        field_map = state.getMap()

        n_rows = field_map.getNumberOfRows()

        # todo expect rectangle shaped playing field
        self.map.x_max = n_rows
        self.map.y_max = field_map.getRowLength(0)

        # wall around field
        for i in range(3):
            self.map.map[WorldPoint(-1, -1, 0)] = Wall(WorldPoint(-1, -1, i), self.asset_storage)

        for x in range(n_rows):
            self.map.map[WorldPoint(x, -1, 1)] = Wall(WorldPoint(x, -1, 0), self.asset_storage)
            self.map.map[WorldPoint(x, -1, 1)] = Wall(WorldPoint(x, -1, 1), self.asset_storage)
            self.map.map[WorldPoint(x, -1, 2)] = Wall(WorldPoint(x, -1, 2), self.asset_storage)

            for y in range(field_map.getRowLength(x)):
                self.map.map[WorldPoint(-1, y, 0)] = Wall(WorldPoint(-1, y, 0), self.asset_storage)
                self.map.map[WorldPoint(-1, y, 1)] = Wall(WorldPoint(-1, y, 1), self.asset_storage)
                self.map.map[WorldPoint(-1, y, 2)] = Wall(WorldPoint(-1, y, 2), self.asset_storage)

        # todo check if coords are right
        for x in range(n_rows):
            for y in range(field_map.getRowLength(x)):
                # add floor --> I don't think this has to be done on each update! todo
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
                    self.map.map[WorldPoint(x, y, z=1)] = Gadget(WorldPoint(x, y, z=1), self.asset_storage)

        # add characters
        for char in state.getCharacters():
            if not char.getCoordinates().has_value():
                continue
            point = char.getCoordinates().value()
            self.map.map[WorldPoint(point.x, point.y, z=1)] = Character(WorldPoint(point.x, point.y, z=1),
                                                                        self.asset_storage)

        # mark active char red.
        active_char = self.controller.lib_client_handler.lib_client.getActiveCharacter()
        active_char_coords = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
            active_char).getCoordinates().value()
        wp_coords = WorldPoint(active_char_coords.x, active_char_coords.y, 0)
        self.map.map[wp_coords].active_char()
        self.map.map[WorldPoint(active_char_coords.x, active_char_coords.y, 2)] = Floor(
            WorldPoint(active_char_coords.x, active_char_coords.y, 2), self.asset_storage)
        self.map.map[WorldPoint(active_char_coords.x, active_char_coords.y, 2)].active_char()
        logging.info("Successfully updated playing field")
