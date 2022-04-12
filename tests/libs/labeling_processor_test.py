""" -*- coding: utf-8 -*-
"""
import unittest

from dotenv import load_dotenv

from config import constants
from src.pear_domain.domain_service.background_remover import BackgroundRemover
from src.pear_domain.domain_service.labeling_processor import LabelingProcessor
from src.pear_domain.domain_service.loader import Loader


class LabelingProcessorTest(unittest.TestCase):

    def test_call(self):
        load_dotenv()
        test_image_directory_path = constants.PROJECT_ROOT_PATH + '/tests/pear_images/1'
        pear = Loader.load_pear(test_image_directory_path)

        background_remover = BackgroundRemover()
        labeling_processor = LabelingProcessor()

        # Pear 型以外を入力した時にレイズすること
        with self.assertRaises(TypeError):
            labeling_processor.call(None)
        with self.assertRaises(TypeError):
            labeling_processor.call([2, 3, 5])

        self.assertIsInstance(labeling_processor, LabelingProcessor)

        background_remover.call(pear)
        labeling_processor.call(pear)

        side_of_pears = pear.side_of_pears
        side_of_pear = side_of_pears[0]

        self.assertNotEqual(side_of_pear.deteriorations, [])


if __name__ == '__main__':
    unittest.main()
