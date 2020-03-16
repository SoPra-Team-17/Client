import unittest

from util.Transforms import Transformations as transforms
import view.ViewConstants as props


class testTrafoToWorldCoords(unittest.TestCase):
    """
    Test will have to be updated when proper gamefield is implemented, for now just checking
    if any changes break the implemented transform on the basic board

    :todo:  should check and depend on resolution of screen! Tests are written for 1920x1080
    :return: None
    """

    def test_without_offset(self):
        xt, yt = transforms.trafo_to_world_coords(1182, 446)
        self.assertEqual((8, 2), (xt, yt))

        xt, yt = transforms.trafo_to_world_coords(993, 571)
        self.assertEqual((9, 9), (xt, yt))

        xt, yt = transforms.trafo_to_world_coords(991, 288)
        self.assertEqual((0, 0), (xt, yt))

        xt, yt = transforms.trafo_to_world_coords(860, 446)
        self.assertEqual((3, 7), (xt, yt))

    def test_with_offset(self):
        xt, yt = transforms.trafo_to_world_coords(525, 364, -12.75, 3.75)
        self.assertEqual((8, 6), (xt, yt))

        xt, yt = transforms.trafo_to_world_coords(1410, 401, 10.0, -3.0)
        self.assertEqual((0, 0), (xt, yt))

        xt, yt = transforms.trafo_to_world_coords(1278, 970, 23.0, 16.0)
        self.assertEqual((3, 1), (xt, yt))

    def test_with_offset_small_diff(self):
        xt, yt = transforms.trafo_to_world_coords(652, 699, -1.5, 11.5)
        self.assertEqual((9, 7), (xt, yt))

        xt, yt = transforms.trafo_to_world_coords(667, 697, -1.5, 11.5)
        self.assertEqual((9, 6), (xt, yt))

        xt, yt = transforms.trafo_to_world_coords(760, 798, 4.75, 10.25)
        self.assertEqual((8, 9), (xt, yt))

        xt, yt = transforms.trafo_to_world_coords(525, 567, -6.0, 7.0)
        self.assertEqual((7, 9), (xt, yt))

    def test_diagonal(self):
        xt, yt = transforms.trafo_to_world_coords(843, 477)
        self.assertEqual((4, 8), (xt, yt))

        xt, yt = transforms.trafo_to_world_coords(818, 479)
        self.assertEqual((3, 9), (xt, yt))

if __name__ == '__main__':
    unittest.main()
