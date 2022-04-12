""" -*- coding: utf-8 -*-

"""

import unittest

import numpy as np

from src.pear_domain.entity.pear import Pear
from src.pear_domain.entity.side_of_pear import SideOfPear


class PearTest(unittest.TestCase):

    def test_set_score(self):
        pear = Pear()
        pear.score = 20.0
        self.assertTrue(pear.score, 20.0)
        with self.assertRaises(ValueError):
            pear.score = None
        with self.assertRaises(TypeError):
            pear.score = 'test'

    def test_add_part_of_pear(self):
        mock_image = np.zeros((224, 224, 3)).astype('float')
        pear = Pear()
        side_of_pear = SideOfPear(mock_image)

        with self.assertRaises(TypeError):
            pear.add_side_of_pear(None)

        for i in range(4):
            pear.add_side_of_pear(side_of_pear)

        with self.assertRaises(ValueError):
            pear.add_side_of_pear(side_of_pear)


if __name__ == '__main__':
    unittest.main()
