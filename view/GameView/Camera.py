from typing import Tuple
import pygame


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

    def center(self) -> None:
        self.__xTrans = 0
        self.__yTrans = 0

    def getTrans(self) -> Tuple[float, float]:
        return self.__xTrans, self.__yTrans
