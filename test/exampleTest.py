import unittest
from controller.Controller import Controller

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        controller = Controller()
        self.assertEqual(controller.someFunc(3,2),5)

    def test_isupper(self):
        controller = Controller()
        self.assertTrue(controller.someFunc(2,0))
        self.assertFalse(controller.someFunc(2,-2))


if __name__ == '__main__':
    unittest.main()