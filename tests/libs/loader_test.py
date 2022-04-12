""" -*- coding: utf-8
"""
import unittest

from config import constants
from src.pear_domain.domain_service.loader import Loader
from src.pear_domain.entity.pear import Pear


class LoadTest(unittest.TestCase):

    def test_load_pear(self):
        test_image_directory_path = constants.PROJECT_ROOT_PATH + '/tests/pear_images/1'
        pear = Loader.load_pear(test_image_directory_path)
        self.assertIsInstance(pear, Pear)
        self.assertEqual(len(pear.side_of_pears), 4)
        self.assertTrue(test_image_directory_path in pear.side_of_pears[0].file_path)

        self.assertEqual('1', pear.side_of_pears[0].get_dir_name())


if __name__ == '__main__':
    unittest.main()
