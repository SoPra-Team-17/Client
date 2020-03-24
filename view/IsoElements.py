from abc import ABC, abstractmethod
from typing import Tuple
from util.Transforms import Transformations
import pygame

"""
Bei diesr Datei handelt es sich nur um eine temporäre Datei, welche die elemtaren isometrischen Module enthält
Später werden diese in ihre eigenen Module eingepflegt
"""


class Drawable(ABC):

    @abstractmethod
    def draw_block(self, window: pygame.display, camOffset: Tuple[float, float]) -> None:
        pass

    @abstractmethod
    def hovering(self, focus: bool = False) -> None:
        pass

    # todo methode kann evtl. auch in der Base Klasse implementiert werden, sollte eigentlich für alle gleich sein
    @abstractmethod
    def __nearness__(self) -> int:
        pass


class Block(Drawable):
    def __init__(self, window: pygame.display, x: int, y: int, z: int) -> None:
        self.window = window

        self.block = pygame.image.load("assets/GameView/block.png")
        self.block = pygame.transform.scale(self.block, (64, 64))

        self.hovered_image = self.block.copy()
        self.hovered_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.hovered_image.fill((0, 255, 0, 0), None, pygame.BLEND_RGBA_ADD)

        self.current_image = self.block

        self.x = x
        self.y = y
        self.z = z

        self.__TILEWIDTH = 64
        self.__TILEHEIGHT = 64
        self.nearness = 0

    def draw_block(self, window: pygame.display, camOffset: Tuple[float, float]) -> None:
        """
        Draw individual Block
        :note see that camera offset is now used in drawing function to keep field coords consistent
        :param window:          pygame display in which the block is drawn
        :param camOffset:       camera perspective
        :return:                None
        """
        self.nearness = self.__nearness__()
        m_x = window.get_rect().centerx
        m_y = window.get_rect().centery
        v_x = (self.x + camOffset[0]) * self.__TILEWIDTH / 2 - (self.y + camOffset[1]) * self.__TILEHEIGHT / 2 + m_x
        v_y = (self.x + camOffset[0]) * self.__TILEWIDTH / 4 + (
                    self.y + camOffset[1]) * self.__TILEHEIGHT / 4 - self.z * self.__TILEHEIGHT / 2 + m_y / 2

        self.window.blit(self.current_image, (v_x, v_y))

    def hovering(self, focus: bool = False) -> None:
        if focus:
            self.current_image = self.hovered_image
        else:
            self.current_image = self.block

    def __nearness__(self) -> int:
        return self.x + self.y + self.z


class BlockGroup:

    def __init__(self) -> None:
        self.list = []

    def add(self, block: Block) -> None:
        self.list.append(block)

    def translation(self, x: float, y: float) -> None:
        for block in self.list:
            block.x += x
            block.y += y

    def sort(self) -> None:
        self.list.sort(key=lambda block: block.nearness)

    def draw(self, window: pygame.display, camOffset: Tuple[float, float]) -> None:
        self.sort()
        for block in self.list:
            block.draw_block(window, camOffset)

    def highlight_block_in_focus(self, camOffset: Tuple[float, float]) -> None:
        pos = pygame.mouse.get_pos()
        offsetX, offsetY = camOffset
        # transform mouse pos to world coords
        xt, yt = Transformations.trafo_window_to_world_coords(pos[0], pos[1], offsetX, offsetY)
        for block in self.list:
            # subtract camera offset from coords to get field coords
            if block.x == xt and block.y == yt and block.z == 0:
                block.hovering(focus=True)
            else:
                block.hovering(focus=False)


class Camera:
    """
    The camera is an isometric camera with a rotation of 45° --> thus all proportions are 2:1
    """

    def __init__(self, camera_speed: float = 1.0, x_factor: float = .5, y_factor: float = 1.0) -> None:
        self.__xTrans = 0
        self.__yTrans = 0
        self.__xFactor = x_factor
        self.__yFactor = y_factor
        self.camera_speed = camera_speed

    def move_camera(self, keys) -> None:
        vx = self.camera_speed * self.__xFactor
        vy = self.camera_speed * self.__yFactor

        if keys[pygame.K_a]:
            self.__xTrans -= vx
            self.__yTrans += vx
        if keys[pygame.K_d]:
            self.__xTrans += vx
            self.__yTrans -= vx
        if keys[pygame.K_w]:
            self.__xTrans -= vy
            self.__yTrans -= vy
        if keys[pygame.K_s]:
            self.__xTrans += vy
            self.__yTrans += vy

    def center(self, block_group: BlockGroup) -> None:
        self.__xTrans = 0
        self.__yTrans = 0

    def getTrans(self) -> Tuple[float, float]:
        return self.__xTrans, self.__yTrans
