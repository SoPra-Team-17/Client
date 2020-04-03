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
        """
        Camera is moved in the direction the key-presses are indicating

        :param keys:    pressed keys provided by `GameViewController`
        :return:        None
        """
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
        """
        Moves Camera back to center
        :return:    None
        """
        self.__xTrans = 0
        self.__yTrans = 0

    def getTrans(self) -> Tuple[float, float]:
        """
        Getter for offset from center
        :return:    Tuple(xTrans, yTrans)
        """
        return self.__xTrans, self.__yTrans
