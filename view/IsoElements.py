from abc import ABC, abstractmethod
import pygame

"""
Bei diesr Datei handelt es sich nur um eine temporäre Datei, welche die elemtaren isometrischen Module enthält
Später werden diese in ihre eigenen Module eingepflegt
"""


class Drawable(ABC):

    @abstractmethod
    def draw_block(self, window: pygame.display):
        pass


class Block(Drawable):
    def __init__(self, window: pygame.display, x: int, y: int, z: int):
        self.window = window

        self.block = pygame.image.load("assets/GameView/block.png")
        self.block = pygame.transform.scale(self.block, (64, 64))

        self.x = x
        self.y = y
        self.z = z

        self.__TILEWIDTH = 64
        self.__TILEHEIGHT = 64
        self.nearness = 0

    def draw_block(self, window: pygame.display):
        self.nearness = self.__nearness__()
        m_x = window.get_rect().centerx
        m_y = window.get_rect().centery
        v_x = self.x * self.__TILEWIDTH / 2 - self.y * self.__TILEHEIGHT / 2 + m_x
        v_y = self.x * self.__TILEWIDTH / 4 + self.y * self.__TILEHEIGHT / 4 - self.z * self.__TILEHEIGHT / 2 + m_y / 2

        self.window.blit(self.block, (v_x, v_y))

    def __nearness__(self):
        return self.x + self.y + self.z


class BlockGroup:

    def __init__(self):
        self.list = []

    def add(self, block: Block):
        self.list.append(block)

    def translation(self, x, y):
        for block in self.list:
            block.x += x
            block.y += y

    def sort(self):
        self.list.sort(key=lambda block: block.nearness)

    def draw(self, window: pygame.display):
        self.sort()
        for block in self.list:
            block.draw_block(window)


class Camera:

    def __init__(self, camera_speed: float = 1.0, x_factor: float = .5, y_factor: float = 1.0):
        self.__xTrans = 0
        self.__yTrans = 0
        self.__xFactor = x_factor
        self.__yFactor = y_factor
        self.camera_speed = camera_speed

    def move_camera(self, keys, block_group: BlockGroup):
        vx = self.camera_speed * self.__xFactor
        vy = self.camera_speed * self.__yFactor

        if keys[pygame.K_a]:
            block_group.translation(-vx, vx)
            self.__xTrans -= vx
            self.__yTrans += vx
        if keys[pygame.K_d]:
            block_group.translation(vx, -vx)
            self.__xTrans += vx
            self.__yTrans -= vx
        if keys[pygame.K_w]:
            block_group.translation(-vy, -vy)
            self.__xTrans -= vy
            self.__yTrans -= vy
        if keys[pygame.K_s]:
            block_group.translation(vy, vy)
            self.__xTrans += vy
            self.__yTrans += vy

    def center(self, block_group: BlockGroup):
        block_group.translation(-self.__xTrans, -self.__yTrans)
        self.__xTrans = 0
        self.__yTrans = 0

    def getTrans(self):
        return self.__xTrans, self.__yTrans
