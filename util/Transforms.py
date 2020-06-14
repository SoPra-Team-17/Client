"""
Implement all needed transforms between coordinate systems
"""
from typing import Tuple
import pygame

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"


class Transformations:

    @staticmethod
    def trafo_window_to_world_coords(x: float, y: float, offsetX: float = 0, offsetY: float = 0) -> Tuple[int, int]:
        """
        Computes transformation from window coordinates to world coordinates (Image->Field)
        :param x:           x-Pos in window
        :param y:           y-Pos in window
        :param offsetX:     offset in x-direction, provided by camera
        :param offsetY:     offset in y-direction, provided by camera
        :return:            (xTrans,yTrans) in world coordinates
        """
        # parameter for tilesize!
        b = h = 64

        xTrans = int((1 / b * x + 2 / b * y + offsetX) // 1 - 24)
        yTrans = int((-1 / h * x + 2 / h * y + offsetY) // 1 + 7)
        return xTrans, yTrans

    @staticmethod
    def trafo_draw_to_screen(pos: Tuple[float, float, float], offset: Tuple[float, float], size: Tuple[int, int],
                             window: pygame.display) -> Tuple[float, float]:
        """
        Computes the transformation to draw an asset onto the playing field
        :param pos:         position on the playing field
        :param offset:      camera offset provided by camera
        :param size:        size of the assets to draw (e.g. 64x64)
        :return:            Tuple where to draw on screen
        """
        x, y, z = pos
        offset_x, offset_y = offset
        tile_height, tile_width = size

        m_x = window.get_rect().centerx
        m_y = window.get_rect().centery

        v_x = (x - offset_x) * tile_width / 2 - (y - offset_y) * tile_height / 2 + m_x
        v_y = (x - offset_x) * tile_width / 4 + (y - offset_y) * tile_height / 4 - z * tile_height / 2 + m_y / 2

        return v_x, v_y
