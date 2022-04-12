""" -*- coding: utf-8
"""

import unittest

from src.pear_domain.value_object.coordinate import Coordinate
from tests import test_util


class SideOfPearTest(unittest.TestCase):

    def test_setter_area(self):
        side_of_pear = test_util.generate_side_of_pear()
        with self.assertRaises(TypeError):
            side_of_pear.area = 'test'

        with self.assertRaises(ValueError):
            side_of_pear.area = None
        side_of_pear.area = 20.0
        self.assertTrue(side_of_pear.area, 20.0)

    def test_setter_contours(self):
        side_of_pear = test_util.generate_side_of_pear()
        with self.assertRaises(TypeError):
            side_of_pear.contours = 'test'
        with self.assertRaises(ValueError):
            side_of_pear.contours = None

    def test_setter_coordinate(self):
        side_of_pear = test_util.generate_side_of_pear()
        with self.assertRaises(TypeError):
            side_of_pear.coordinate = 'test'
        with self.assertRaises(ValueError):
            side_of_pear.coordinate = None

        coordinate = test_util.generate_coordinate()
        side_of_pear.coordinate = coordinate
        self.assertIsInstance(side_of_pear.coordinate, Coordinate)

    def test_calculate_area_rate_deterioration(self):
        side_of_pear = test_util.generate_side_of_pear()
        coordinate = test_util.generate_coordinate()
        coordinate.pixel = 100.0
        side_of_pear.area = 200.0
        area_rate = side_of_pear.calculate_area_rate(coordinate)
        self.assertEqual(0.5, area_rate)

    def test_add_deterioration(self):
        side_of_pear = test_util.generate_side_of_pear()
        deterioration = test_util.generate_deterioration()
        side_of_pear.add_deterioration(deterioration)
        self.assertTrue(deterioration, side_of_pear.deteriorations[0])
        with self.assertRaises(TypeError):
            side_of_pear.add_deterioration('test')


if __name__ == '__main__':
    unittest.main()
