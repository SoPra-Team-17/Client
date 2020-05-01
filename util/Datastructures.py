"""
Implements a datastructure to store the current representation of the playing field (in drawable elements)
"""
import string
from typing import Tuple
import numpy as np

from util.Coordinates import WorldPoint
from view.GameView.Drawable import Drawable

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"


class DrawableMap:

    def __init__(self, dims: Tuple[int, int, int] = (100, 100, 10)) -> None:
        self._list = [None] * np.array(dims).prod()
        self._dims = dims

    def __getitem__(self, item: WorldPoint) -> Drawable:
        """
        Overrides __getitem__ to return a drawable from list given a WorldPoint
        :param item:    Worldpoint used to index list
        :return:        Drawabled retrieved from list
        """
        return self._list[self._get_index(item)]

    def __setitem__(self, item: WorldPoint, value: Drawable) -> None:
        """
        Overrides __setitem__ to insert a Drawable in a list given a Worldpoint
        :param item:    Worldpoint used to index list
        :param value:   Drawable to be inserted
        :return:        None
        """
        self._list[self._get_index(item)] = value

    def __len__(self) -> int:
        """
        Returns length of list, which in this case is the volume of the cuboid
        :return:    Length of self.list
        """
        return len(self._list)

    def __repr__(self) -> string:
        return f"DawableList Length: {self.__len__()}"

    def __contains__(self, item: Drawable) -> bool:
        """
        Overrides __contains__, used for membership test. Returns true when object exists
        :param item:    Object to be tested
        :return:        True/False
        """
        return item in self._list

    def _get_index(self, item: WorldPoint) -> int:
        """
        Maps three dimensional coords to one dimensonal list index
        :param item:    input/index WorldPoint
        :return:        index in list
        """
        return item.x + item.y * self._dims[0] + item.z * self._dims[0] * self._dims[1]
