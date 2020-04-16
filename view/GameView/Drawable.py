from typing import Tuple
from abc import ABC, abstractmethod
from view.GameView.AssetStorage import BlockAssets, AssetStorage
from view.ViewSettings import ViewSettings
from util.Transforms import Transformations
from util.Coordinates import WorldPoint
import pygame


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

    def __nearness__(self) -> int:
        return self.point.x + self.point.y + self.point.z


class DrawableGroup:

    def __init__(self, settings: ViewSettings) -> None:
        self.list = []
        self.settings = settings

    def add(self, drawable: Drawable) -> None:
        self.list.append(drawable)

    def translation(self, offSet: Tuple[float, float]) -> None:
        for drawable in self.list:
            drawable.point.x += offSet[0]
            drawable.point.y += offSet[1]

    def sort(self) -> None:
        self.list.sort(key=lambda drawable: drawable.nearness)

    def draw(self, window: pygame.display, camOffset: Tuple[float, float]) -> None:
        self.sort()
        for drawable in self.list:
            drawable.draw(window, camOffset, self.settings)

    def highlight_drawable_in_focus(self, camOffset: Tuple[float, float]) -> None:
        pos = pygame.mouse.get_pos()
        # transform mouse pos to world coords
        xt, yt = Transformations.trafo_window_to_world_coords(pos[0], pos[1], -camOffset[0], -camOffset[1])
        # todo create map to access in O(1) instead of O(n)
        for drawable in self.list:
            if drawable.point.x == xt and drawable.point.y == yt and drawable.point.z == 0:
                drawable.hovering(focus=True)
            else:
                drawable.hovering(focus=False)


class Block(Drawable):
    def __init__(self, window: pygame.display, pos: WorldPoint, assets: AssetStorage) -> None:
        super(Block, self).__init__(pos, assets)

        self.window = window

        self.block = self.asset_storage.block_assets.block_image
        self.hovered_image = self.asset_storage.block_assets.hovered_image

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
