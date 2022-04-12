# -*- config: utf-8 -*-

import unittest

from config import constants

from src.pear_domain.domain_service.loader import Loader
from src.pear_domain.value_object.deterioration import Deterioration
from src.pear_domain.application_service.pear_grade_evaluator import PearGradeEvaluator

from tests import test_util


class PearGradeEvaluatorTest(unittest.TestCase):
    def test_call(self):
        pear_grade_evaluator = PearGradeEvaluator()

        test_image_directory_path = constants.PROJECT_ROOT_PATH + '/tests/pear_images/1'
        pear = Loader.load_pear(test_image_directory_path)

        for side_of_pear in pear.side_of_pears:
            side_of_pear.area = 5000.0
            coordinate = test_util.generate_coordinate()
            coordinate.pixel = 20.0
            area_rate = side_of_pear.calculate_area_rate(coordinate)
            deterioration = Deterioration(area_rate=area_rate, deterioration_class=2, coordinate=coordinate)
            side_of_pear.add_deterioration(deterioration)

        pear_grade_evaluator.call(pear)

        self.assertTrue(pear)


if __name__ == '__main__':
    unittest.main()
