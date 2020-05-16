"""
Implements actual playing field
"""
import logging
import pygame

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


def create_playing_field(map, assets: AssetStorage) -> None:
    """
    Methode used for testing, generates basic field to test transformations and so on
    :todo can be deleted as soon as scenario files can be read in
    :param group:
    :param window:
    :return:
    """

    map[WorldPoint(0, 0, 1)] = Wall(WorldPoint(0, 0, 1), assets)
    map[WorldPoint(0, 0, 2)] = Wall(WorldPoint(0, 0, 2), assets)

    map[WorldPoint(3, 2, 1)] = Wall(WorldPoint(3, 2, 1), assets)
    map[WorldPoint(3, 2, 2)] = Wall(WorldPoint(3, 2, 2), assets)

    map[WorldPoint(4, 4, 1)] = Fireplace(WorldPoint(4, 4, 1), assets)

    map[WorldPoint(2, 4, 1)] = RouletteTable(WorldPoint(2, 4, 1), assets)

    map[WorldPoint(0, 4, 1)] = BarSeat(WorldPoint(0, 4, 1), assets)

    map[WorldPoint(4, 0, 1)] = Character(WorldPoint(4, 0, 1), assets)

    map[WorldPoint(6, 0, 1)] = Gadget(WorldPoint(6, 0, 1), assets)

    map[WorldPoint(6, 6, 1)] = BarTable(WorldPoint(6, 6, 1), assets)

    map[WorldPoint(7, 2, 1)] = Safe(WorldPoint(7, 2, 1), assets)

    for i in range(0, 50, 1):
        for j in range(0, 50, 1):
            map[WorldPoint(i, j, 0)] = Floor(WorldPoint(i, j, 0), assets)

    for x in range(50):
        map[WorldPoint(x, -1, 1)] = Wall(WorldPoint(x, -1, 0), assets)
        map[WorldPoint(x, -1, 1)] = Wall(WorldPoint(x, -1, 1), assets)
        map[WorldPoint(x, -1, 2)] = Wall(WorldPoint(x, -1, 2), assets)

    for y in range(50):
        map[WorldPoint(-1, y, 0)] = Wall(WorldPoint(-1, y, 0), assets)
        map[WorldPoint(-1, y, 1)] = Wall(WorldPoint(-1, y, 1), assets)
        map[WorldPoint(-1, y, 2)] = Wall(WorldPoint(-1, y, 2), assets)


class PlayingFieldScreen(BasicView):
    """
    This class contains all the relevant information for drawing the gameview
    """

    def __init__(self, window: pygame.display, controller, parent_view, settings: ViewSettings):
        super(PlayingFieldScreen, self).__init__(window, controller, settings)

        self.parent_view = parent_view

        self.asset_storage = AssetStorage()
        self.camera = self.camera = Camera(camera_speed=.5)

        map = DrawableMap((50, 50, 3))
        create_playing_field(map, assets=self.asset_storage)

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
        import cppyy
        state = self.controller.lib_client_handler.lib_client.getState()
        field_map = state.getMap()

        n_rows = field_map.getNumberOfRows()
        n_cols = field_map.getRowLength()

        # wall around field
        for x in range(n_rows):
            self.map.map[WorldPoint(x, -1, 1)] = Wall(WorldPoint(x, -1, 0), self.asset_storage)
            self.map.map[WorldPoint(x, -1, 1)] = Wall(WorldPoint(x, -1, 1), self.asset_storage)
            self.map.map[WorldPoint(x, -1, 2)] = Wall(WorldPoint(x, -1, 2), self.asset_storage)

        for y in range(n_cols):
            self.map.map[WorldPoint(-1, y, 0)] = Wall(WorldPoint(-1, y, 0), self.asset_storage)
            self.map.map[WorldPoint(-1, y, 1)] = Wall(WorldPoint(-1, y, 1), self.asset_storage)
            self.map.map[WorldPoint(-1, y, 2)] = Wall(WorldPoint(-1, y, 2), self.asset_storage)

        # todo check if coords are right
        for x in range(n_rows):
            for y in range(n_cols):
                # add floor --> I don't think this has to be done on each update! todo
                self.map.map[WorldPoint(x, y, z=0)] = Floor(WorldPoint(x, y, z=0), self.asset_storage)

                field = field_map.getField(x, y)

                state = field.getFieldState()
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
                    if state is not None:
                        self.map.map[WorldPoint(x, y, z=1)] = switcher.get(state)(WorldPoint(x, y, z=1),
                                                                                  self.asset_storage)
                except TypeError:
                    logging.error("Unable to find correct element in dict")

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
