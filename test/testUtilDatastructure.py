"""
Class testing the datastructure used to hold the playing field and its drawables
"""
import unittest

from util.Datastructures import DrawableMap
from util.Coordinates import WorldPoint

__author__ = "Marco Deuscher"
__date__ = "12.06.2020"


class testUtilDatastructure(unittest.TestCase):

    def test_size(self):
        dmap = DrawableMap((100, 100, 10))
        self.assertEqual(len(dmap), 100 * 100 * 10)

    def test_set_item(self):
        dmap = DrawableMap((10, 10, 10))
        dmap[WorldPoint(1, 1, 1)] = 17
        self.assertEqual(dmap[WorldPoint(1, 1, 1)], 17)

    def test_get_item(self):
        dmap = DrawableMap((10, 10, 10))
        self.assertIsNone(dmap[WorldPoint(0, 0, 0)])

        dmap[WorldPoint(1, 1, 1)] = 42
        self.assertEqual(dmap[WorldPoint(1, 1, 1)], 42)

    def test_contains(self):
        dmap = DrawableMap((10, 10, 10))
        dmap[WorldPoint(1, 1, 1)] = 17
        self.assertTrue(dmap.__contains__(17))

        self.assertFalse(dmap.__contains__(42))

    def test_repr(self):
        dmap = DrawableMap((10, 10, 10))
        self.assertEqual(dmap.__repr__(), f"DrawableList Length: {len(dmap)}")
