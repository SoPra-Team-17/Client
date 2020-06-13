"""
Class testing the implemented worldpoint
"""
import unittest

from util.Coordinates import WorldPoint

__author__ = "Marco Deuscher"
__date__ = "12.06.2020"


class testUtilCoordinates(unittest.TestCase):

    def test_setting_values(self):
        wp = WorldPoint(x=1, y=2, z=3)
        self.assertTrue(wp.x == 1 and wp.y == 2 and wp.z == 3, "All values equal")

        wp.x = 10
        wp.y = 11
        wp.z = 12
        self.assertTrue(wp.x == 10 and wp.y == 11 and wp.z == 12, "All values equal")

    def test_equality(self):
        wp1 = WorldPoint(x=1, y=2, z=3)
        wp2 = WorldPoint(x=1, y=2, z=3)
        self.assertTrue(wp1 == wp2, "Points are equal")
        self.assertFalse(wp1 != wp2, "Points are equal")

        wp1 = WorldPoint(x=1, y=2, z=3)
        wp2 = WorldPoint()
        self.assertFalse(wp1 == wp2, "Points are not equal")
        self.assertTrue(wp1 != wp2, "Points are not equal")

        wp1 = WorldPoint()
        wp2 = None
        self.assertFalse(wp1 == wp2, "Other is none")
        self.assertRaises(TypeError, wp2 == wp1)

    def test_repr(self):
        wp1_str = WorldPoint().__repr__()
        self.assertEqual(wp1_str, "x: 0 y: 0 z: 0")

        wp2_str = WorldPoint(x=1, y=2, z=3).__repr__()
        self.assertEqual(wp2_str, "x: 1 y: 2 z: 3")
