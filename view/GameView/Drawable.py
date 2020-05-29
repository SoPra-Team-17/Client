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

    def __init__(self, pos: WorldPoint = None, asset_storage: AssetStorage = None, size: Tuple[int, int] = (64, 64)):
        self.current_image = None
        self.asset_storage = asset_storage
        self.point = WorldPoint() if pos is None else pos
        self.__TILEHEIGHT, self.__TILEWIDTH = size

    def draw(self, window: pygame.display, camOffset: Tuple[float, float], settings: ViewSettings) -> None:
        """
        Draw individual Block
        :note see that camera offset is now used in drawing function to keep field coords consistent
        :param settings:        settings object, containing window size, fps, etc.
        :param window:          pygame display in which the block is drawn
        :param camOffset:       camera perspective
        :return:                None
        """
        v_x, v_y = Transformations.trafo_draw_to_screen((self.point.x, self.point.y, self.point.z), camOffset,
                                                        (self.__TILEHEIGHT, self.__TILEWIDTH), window)

        # only draw block, when still inside visible window! accout for block size so block is not clipped on the edge
        if -64 <= v_x <= settings.window_width + 64 and -64 <= v_y <= settings.window_height:
            window.blit(self.current_image, (v_x, v_y))

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

        # todo expect rectangle shaped playing fieldd D
        self.x_max = 0
        self.y_max = 0

    def get_selected_coords(self) -> WorldPoint:
        return self.__selected_coords if self.__selected_coords != WorldPoint(0, 0, 0) else None

    def translation(self, offset: Tuple[float, float]) -> None:
        for drawable in self.map.list:
            if drawable is not None:
                drawable.point.x += offset[0]
                drawable.point.y += offset[1]

    def draw(self, window: pygame.display, camOffset: Tuple[float, float]) -> None:
        # self.sort() --> siehe sort comment
        for drawable in self.map.list:
            if drawable is not None:
                drawable.draw(window, camOffset, self.settings)

    def highlight_drawable_in_focus(self, camOffset: Tuple[float, float]) -> None:
        """
        Highlight the block of the floor which is currently focused
        :param camOffset:
        :return:
        """
        pos = pygame.mouse.get_pos()
        # transform mouse pos to world coords
        xt, yt = Transformations.trafo_window_to_world_coords(pos[0], pos[1], camOffset[0], camOffset[1])

        if xt < 0 or xt >= self.x_max or yt < 0 or yt >= self.y_max:
            return

        if self.__selected_coords != self.__hovered_coords:
            self.map[self.__hovered_coords].hovering(False)

        self.__hovered_coords = WorldPoint(xt, yt, 0)

        if self.__selected_coords != self.__hovered_coords:
            self.map[self.__hovered_coords].hovering(True)

    def select_block(self, camOffset: Tuple[float, float]) -> None:
        """
        Processes mouse click on playing field and gets coordinates of selected block (always on the floor)
        :param camOffset:   camera offset provided by camera
        :return:            None (sets attribute __selected_coords)
        """
        self.map[self.__selected_coords].selected(False)

        pos = pygame.mouse.get_pos()
        # transform mouse pos to world coords
        xt, yt = Transformations.trafo_window_to_world_coords(pos[0], pos[1], camOffset[0], camOffset[1])

        if xt < 0 or xt >= self.map.dims[0] or yt < 0 or yt >= self.map.dims[1]:
            return
        selected = WorldPoint(xt, yt, 0)
        if selected != self.__selected_coords:
            self.__selected_coords = WorldPoint(xt, yt, 0)
            self.map[self.__selected_coords].selected(True)
        else:
            self.map[self.__selected_coords].selected(False)
            # todo point (0,0,0) will not work properly
            self.__selected_coords = WorldPoint()


class Floor(Drawable):
    def __init__(self, pos: WorldPoint, assets: AssetStorage) -> None:
        super(Floor, self).__init__(pos, assets, (64, 64))

        self.block = self.asset_storage.block_assets.block_image
        self.hovered_image = self.asset_storage.block_assets.hovered_image
        self.selected_image = self.asset_storage.block_assets.selected_image
        self.active_char_image = self.asset_storage.block_assets.active_char_image

        self.current_image = self.block

    def hovering(self, focus: bool = False) -> None:
        self.current_image = self.hovered_image if focus else self.block

    def selected(self, selected: bool = False) -> None:
        self.current_image = self.selected_image if selected else self.block

    def active_char(self):
        self.current_image = self.active_char_image


class Wall(Drawable):
    def __init__(self, pos: WorldPoint, assets: AssetStorage) -> None:
        super(Wall, self).__init__(pos, assets, (64, 64))

        self.block = self.asset_storage.wall_assets.block_image
        self.current_image = self.block

    def hovering(self, focus: bool = False) -> None:
        pass

    def selected(self, selected: bool = False) -> None:
        pass


class Fireplace(Drawable):

    def __init__(self, pos: WorldPoint, assets: AssetStorage) -> None:
        super(Fireplace, self).__init__(pos, assets, (64, 64))

        self.block = assets.fireplace_assets.block_image
        self.current_image = self.block

    def hovering(self, focus: bool = False) -> None:
        pass

    def selected(self, selected: bool = False) -> None:
        pass


class RouletteTable(Drawable):
    def __init__(self, pos: WorldPoint, assets: AssetStorage) -> None:
        super(RouletteTable, self).__init__(pos, assets, (64, 64))

        self.block = assets.roulettetable_assets.block_image
        self.current_image = self.block

    def hovering(self, focus: bool = False) -> None:
        pass

    def selected(self, selected: bool = False) -> None:
        pass


class BarSeat(Drawable):
    def __init__(self, pos: WorldPoint, assets: AssetStorage) -> None:
        super(BarSeat, self).__init__(pos, assets, (64, 64))

        self.block = self.asset_storage.barseat_assets.block_image
        self.current_image = self.block

    def hovering(self, focus: bool = False) -> None:
        pass

    def selected(self, selected: bool = False) -> None:
        pass


class BarTable(Drawable):
    def __init__(self, pos: WorldPoint, assets: AssetStorage) -> None:
        super(BarTable, self).__init__(pos, assets, (64, 64))

        self.block = self.asset_storage.bartable_assets.block_image
        self.current_image = self.block

    def hovering(self, focus: bool = False) -> None:
        pass

    def selected(self, selected: bool = False) -> None:
        pass


class Character(Drawable):
    def __init__(self, pos: WorldPoint, assets: AssetStorage) -> None:
        super(Character, self).__init__(pos, assets, (64, 64))

        self.block = self.asset_storage.character_assets.block_image
        self.current_image = self.block

    def hovering(self, focus: bool = False) -> None:
        pass

    def selected(self, selected: bool = False) -> None:
        pass


class Gadget(Drawable):
    def __init__(self, pos: WorldPoint, assets: AssetStorage) -> None:
        super(Gadget, self).__init__(pos, assets, (64, 64))

        self.block = self.asset_storage.gadget_assets.block_image
        self.current_image = self.block

    def hovering(self, focus: bool = False) -> None:
        pass

    def selected(self, selected: bool = False) -> None:
        pass


class Safe(Drawable):
    def __init__(self, pos: WorldPoint, assets: AssetStorage) -> None:
        super(Safe, self).__init__(pos, assets, (64, 64))

        self.block = self.asset_storage.safe_assets.block_image
        self.current_image = self.block

    def hovering(self, focus: bool = False) -> None:
        pass

    def selected(self, selected: bool = False) -> None:
        pass


class Fog(Drawable):
    def __init__(self, pos: WorldPoint, assets: AssetStorage) -> None:
        super(Fog, self).__init__(pos, assets, (64, 64))

        self.block = self.asset_storage.fog_assets.block_image
        self.current_image = self.block

    def hovering(self, focus: bool = False) -> None:
        pass

    def selected(self, selected: bool = False) -> None:
        pass


class Janitor(Drawable):
    def __init__(self, pos: WorldPoint, assets: AssetStorage) -> None:
        super(Janitor, self).__init__(pos, assets, (64, 64))

        self.block = self.asset_storage.janitor_assets.block_image
        self.current_image = self.block

    def hovering(self, focus: bool = False) -> None:
        pass

    def selected(self, selected: bool = False) -> None:
        pass


class Cat(Drawable):
    def __init__(self, pos: WorldPoint, assets: AssetStorage) -> None:
        super(Cat, self).__init__(pos, assets, (64, 64))

        self.block = self.asset_storage.cat_assets.block_image
        self.current_image = self.block

    def hovering(self, focus: bool = False) -> None:
        pass

    def selected(self, selected: bool = False) -> None:
        pass
