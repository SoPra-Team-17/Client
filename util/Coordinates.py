"""
Implements a Point in a 3D discrete coordinate system
"""

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"


class WorldPoint:
    def __init__(self, x: int = 0, y: int = 0, z: int = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other) -> bool:
        """
        Checks equality of two points
        :param other:   other Worldpoint
        :return:        True if x1==x2, y1==y2, z1==z2
        """
        if other is None:
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self) -> str:
        """
        Creates a string representation of the object
        Can be used for debugging
        :return:    String
        """
        return f"x: {self.x} y: {self.y} z: {self.z}"
