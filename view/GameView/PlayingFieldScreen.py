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

    map[WorldPoint(0, 0, 1)] = Block(WorldPoint(0, 0, 1), assets)
    map[WorldPoint(0, 0, 2)] = Block(WorldPoint(0, 0, 2), assets)

    map[WorldPoint(3, 2, 1)] = Block(WorldPoint(3, 2, 1), assets)
    map[WorldPoint(3, 2, 2)] = Block(WorldPoint(3, 2, 2), assets)

    map[WorldPoint(4, 4, 1)] = Fireplace(WorldPoint(4, 4, 1), assets)

    map[WorldPoint(2, 4, 1)] = RouletteTable(WorldPoint(2, 4, 1), assets)

    map[WorldPoint(0, 4, 1)] = BarSeat(WorldPoint(0, 4, 1), assets)

    map[WorldPoint(4, 0, 1)] = Character(WorldPoint(4, 0, 1), assets)

    map[WorldPoint(6, 0, 1)] = Gadget(WorldPoint(6, 0, 1), assets)

    for i in range(0, 50, 1):
        for j in range(0, 50, 1):
            map[WorldPoint(i, j, 0)] = Block(WorldPoint(i, j, 0), assets)


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
