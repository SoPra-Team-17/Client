"""
Implements actual playing field
"""
import logging
import pygame

from view.BasicView import BasicView
from view.GameView.Drawable import Block, FieldMap
from view.GameView.Camera import Camera
from view.GameView.AssetStorage import AssetStorage
from view.ViewSettings import ViewSettings
from util.Transforms import Transformations
from util.Coordinates import WorldPoint
from util.Datastructures import DrawableMap

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"


def create_playing_field(map, window: pygame.display, assets: AssetStorage) -> None:
    """
    Methode used for testing, generates basic field to test transformations and so on
    :todo can be deleted as soon as scenario files can be read in
    :param group:
    :param window:
    :return:
    """

    for i in range(0, 50, 1):
        for j in range(0, 50, 1):
            # group.add(Block(window, WorldPoint(i, j, 0), assets))
            map[WorldPoint(i, j, 0)] = Block(window, WorldPoint(i, j, 0), assets)


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
        create_playing_field(map, self.window, assets=self.asset_storage)

        self.map = FieldMap(settings)
        self.map.map = map

    def draw(self):
        self.camera.move_camera(pygame.key.get_pressed())
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

