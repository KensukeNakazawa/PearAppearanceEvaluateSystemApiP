""" -*- coding: utf-8 -*-
"""

import unittest

from config.constants import DETERIORATION_CLASSES
from tests import test_util


class DeteriorationTest(unittest.TestCase):

    def test_setter_area_rate(self):
        deterioration = test_util.generate_deterioration()
        deterioration.area_rate = 20.0
        self.assertTrue(deterioration.area_rate, 20.0)
        with self.assertRaises(ValueError):
            deterioration.area_rate = None
        with self.assertRaises(TypeError):
            deterioration.area_rate = 'test'

    def test_setter_deterioration_class(self):
        deterioration = test_util.generate_deterioration()
        deterioration.deterioration_class = 1
        self.assertTrue(deterioration.deterioration_class, 1)
        with self.assertRaises(ValueError):
            deterioration.deterioration_class = None
        with self.assertRaises(TypeError):
            deterioration.deterioration_class = 'test'
        with self.assertRaises(ValueError):
            deterioration.deterioration_class = DETERIORATION_CLASSES[-1] + 1
        with self.assertRaises(ValueError):
            deterioration.deterioration_class = DETERIORATION_CLASSES[0] - 1

    def test_setter_coordinate(self):
        deterioration = test_util.generate_deterioration()
        coordinate = test_util.generate_coordinate()
        deterioration.coordinate = coordinate
        self.assertTrue(coordinate, deterioration.coordinate)
        with self.assertRaises(ValueError):
            deterioration.coordinate = None
        with self.assertRaises(TypeError):
            deterioration.coordinate = 'test'


if __name__ == '__main__':
    unittest.main()
