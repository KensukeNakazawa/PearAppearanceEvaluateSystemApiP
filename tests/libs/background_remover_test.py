""" -*- coding: utf:8 -*-
"""

import unittest

from config import constants
from src.pear_domain.domain_service.background_remover import BackgroundRemover
from src.pear_domain.domain_service.loader import Loader

from src.pear_domain.value_object.coordinate import Coordinate


class BackgroundRemoverTest(unittest.TestCase):

    def test_call(self):
        background_remover = BackgroundRemover()

        # Pear型以外のデータが入った時にレイズすること
        with self.assertRaises(TypeError):
            background_remover.call(1)
        with self.assertRaises(TypeError):
            background_remover.call(None)

        test_image_directory_path = constants.PROJECT_ROOT_PATH + '/tests/pear_images/1'
        pear = Loader.load_pear(test_image_directory_path)

        # 何もする前は空であること
        for side_of_pear in pear.side_of_pears:
            self.assertEqual(side_of_pear.coordinate, None)

        background_remover.call(pear)
        # 背景除去した後は各洋ナシの側面の情報の中に，洋ナシの輪郭を含む座標の情報があること
        for side_of_pear in pear.side_of_pears:
            self.assertIsInstance(side_of_pear.coordinate, Coordinate)


if __name__ == '__main__':
    unittest.main()
