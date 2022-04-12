""" -*- coding: utf-8 -*-
"""

import unittest

from tests import test_util


class CoordinateTest(unittest.TestCase):

    def test_setter_under(self):
        coordinate = test_util.generate_coordinate()
        coordinate.under = 30
        self.assertTrue(coordinate.under, 30)
        with self.assertRaises(ValueError):
            coordinate.under = None

        with self.assertRaises(TypeError):
            coordinate.under = 'test'

    def test_setter_top(self):
        coordinate = test_util.generate_coordinate()
        coordinate.top = 30
        self.assertTrue(coordinate.top, 30)
        with self.assertRaises(ValueError):
            coordinate.top = None

        with self.assertRaises(TypeError):
            coordinate.top = 'test'

    def test_setter_right(self):
        coordinate = test_util.generate_coordinate()
        coordinate.right = 30
        self.assertTrue(coordinate.right, 30)
        with self.assertRaises(ValueError):
            coordinate.right = None
        with self.assertRaises(TypeError):
            coordinate.right = 'test'

    def test_setter_left(self):
        coordinate = test_util.generate_coordinate()
        coordinate.left = 30
        self.assertTrue(coordinate.left, 30)
        with self.assertRaises(ValueError):
            coordinate.left = None
        with self.assertRaises(TypeError):
            coordinate.left = 'test'

    def test_setter_pixel(self):
        coordinate = test_util.generate_coordinate()
        coordinate.pixel = 30.0
        self.assertTrue(coordinate.pixel, 30.0)
        with self.assertRaises(ValueError):
            coordinate.pixel = None
        with self.assertRaises(TypeError):
            coordinate.pixel = 'test'


if __name__ == '__name__':
    unittest.main()
