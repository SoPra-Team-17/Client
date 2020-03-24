from typing import Tuple

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

        xTrans = int((1 / b * x + 2 / b * y - offsetX) // 1 - 24)
        yTrans = int((-1 / h * x + 2 / h * y - offsetY) // 1 + 7)
        return xTrans, yTrans