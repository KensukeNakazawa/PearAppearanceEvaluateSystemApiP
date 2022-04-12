""" -*- coding: utf-8 -*-
"""
import unittest

from dotenv import load_dotenv

from config import constants
from src.pear_domain.domain_service.loader import Loader
from src.pear_domain.domain_service.deterioration_classifier import DeteriorationClassifier
from src.pear_domain.domain_service.labeling_processor import LabelingProcessor
from src.pear_domain.domain_service.background_remover import BackgroundRemover


class DeteriorationClassifierTest(unittest.TestCase):

    def test_call(self):
        load_dotenv()
        test_image_directory_path = constants.PROJECT_ROOT_PATH + '/tests/pear_images/1'
        pear = Loader.load_pear(test_image_directory_path)

        background_remover = BackgroundRemover()
        labeling_processor = LabelingProcessor()
        deterioration_classifier = DeteriorationClassifier()

        background_remover.call(pear)
        labeling_processor.call(pear)
        deterioration_classifier.call(pear)

        for side_of_pear in pear.side_of_pears:
            for deterioration in side_of_pear.deteriorations:
                self.assertIsNotNone(deterioration.deterioration_class)


if __name__ == '__main__':
    unittest.main()
