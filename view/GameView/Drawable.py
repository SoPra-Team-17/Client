"""
Defines the abstract class of a drawable and contains implementations of Drawables
"""
from typing import Tuple
from abc import ABC, abstractmethod
import pygame

from view.GameView.AssetStorage import AssetStorage
from view.ViewSettings import ViewSettings
from util.Transforms import Transformations
from util.Coordinates import WorldPoint
from util.Datastructures import DrawableMap

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"


class Drawable(ABC):

    def __init__(self, pos: WorldPoint = None, asset_storage: AssetStorage = None):
        self.nearness = 0
        self.asset_storage = asset_storage
        self.point = WorldPoint() if pos is None else pos

    @abstractmethod
    def draw(self, window: pygame.display, camOffset: Tuple[float, float], settings: ViewSettings) -> None:
        pass

    @abstractmethod
    def hovering(self, focus: bool = False) -> None:
        pass

    @abstractmethod
    def selected(self, selected: bool = False) -> None:
        pass

    def __nearness__(self) -> int:
        return self.point.x + self.point.y + self.point.z


class FieldMap:
    def __init__(self, settings: ViewSettings) -> None:
        self.map = DrawableMap()
        self.settings = settings

        self.__hovered_coords = WorldPoint()
        self.__selected_coords = WorldPoint()

    def translation(self, offset: Tuple[float, float]) -> None:
        for drawable in self.map.list:
            if drawable is not None:
                drawable.point.x += offset[0]
                drawable.point.y += offset[1]

    def sort(self) -> None:
        """
        todo ich glaube mit der neuen Datenstruktur ist das sortieren nicht mehr notwendig!
        :return:
        """
        self.map.list.sort(key=lambda drawable: drawable.nearness if drawable is not None else 9999999)

    def draw(self, window: pygame.display, camOffset: Tuple[float, float]) -> None:
        # self.sort() --> siehe sort comment
        for drawable in self.map.list:
            if drawable is not None:
                drawable.draw(window, camOffset, self.settings)

    def highlight_drawable_in_focus(self, camOffset: Tuple[float, float]) -> None:
        pos = pygame.mouse.get_pos()
        # transform mouse pos to world coords
        xt, yt = Transformations.trafo_window_to_world_coords(pos[0], pos[1], camOffset[0], camOffset[1])

        # todo hardcoded check if inside field!
        if xt < 0 or xt >= 50 or yt < 0 or yt >= 50:
            return

        if self.__selected_coords != self.__hovered_coords:
            self.map[self.__hovered_coords].hovering(False)

        self.__hovered_coords = WorldPoint(xt, yt, 0)

        if self.__selected_coords != self.__hovered_coords:
            self.map[self.__hovered_coords].hovering(True)

    def select_block(self, camOffset: Tuple[float, float]) -> None:
        self.map[self.__selected_coords].selected(False)

        pos = pygame.mouse.get_pos()
        # transform mouse pos to world coords
        xt, yt = Transformations.trafo_window_to_world_coords(pos[0], pos[1], camOffset[0], camOffset[1])

        # todo hardcoded check if inside field!
        if xt < 0 or xt >= 50 or yt < 0 or yt >= 50:
            return
        selected = WorldPoint(xt, yt, 0)
        if selected != self.__selected_coords:
            self.__selected_coords = WorldPoint(xt, yt, 0)
            self.map[self.__selected_coords].selected(True)
        else:
            self.map[self.__selected_coords].selected(False)
            self.__selected_coords = WorldPoint()


class Block(Drawable):
    def __init__(self, window: pygame.display, pos: WorldPoint, assets: AssetStorage) -> None:
        super(Block, self).__init__(pos, assets)

        self.window = window

        self.block = self.asset_storage.block_assets.block_image
        self.hovered_image = self.asset_storage.block_assets.hovered_image
        self.selected_image = self.asset_storage.block_assets.selected_image

        self.current_image = self.block

        self.__TILEWIDTH = 64
        self.__TILEHEIGHT = 64

    def draw(self, window: pygame.display, camOffset: Tuple[float, float], settings: ViewSettings) -> None:
        """
        Draw individual Block
        :note see that camera offset is now used in drawing function to keep field coords consistent
        :param settings:        settings object, containing window size, fps, etc.
        :param window:          pygame display in which the block is drawn
        :param camOffset:       camera perspective
        :return:                None
        """
        self.nearness = self.__nearness__()
        m_x = window.get_rect().centerx
        m_y = window.get_rect().centery
        v_x = (self.point.x - camOffset[0]) * self.__TILEWIDTH / 2 - (
                self.point.y - camOffset[1]) * self.__TILEHEIGHT / 2 + m_x
        v_y = (self.point.x - camOffset[0]) * self.__TILEWIDTH / 4 + (
                self.point.y - camOffset[
            1]) * self.__TILEHEIGHT / 4 - self.point.z * self.__TILEHEIGHT / 2 + m_y / 2

        # only draw block, when still inside visible window! accout for block size so block is not clipped on the edge
        if -64 <= v_x <= settings.window_width + 64 and -64 <= v_y <= settings.window_height:
            self.window.blit(self.current_image, (v_x, v_y))

    def hovering(self, focus: bool = False) -> None:
        if focus:
            self.current_image = self.hovered_image
        else:
            self.current_image = self.block

    def selected(self, selected: bool = False) -> None:
        if selected:
            self.current_image = self.selected_image
        else:
            self.current_image = self.block
