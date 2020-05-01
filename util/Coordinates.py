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
