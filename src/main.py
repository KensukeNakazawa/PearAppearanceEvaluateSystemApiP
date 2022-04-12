# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from dotenv import load_dotenv

from config import constants
from src.pear_domain.domain_service.loader import Loader

from src.pear_domain.application_service.pear_deterioration_detector import PearDeteriorationDetector
from src.pear_domain.application_service.pear_grade_evaluator import PearGradeEvaluator
from src.pear_domain.application_service.pear_deterioration_writer import PearDeteriorationWriter


def main():
    image_root_dir = constants.PROJECT_ROOT_PATH + '/images/original_images/'
    directories = os.listdir(image_root_dir)

    pear_deterioration_detector = PearDeteriorationDetector()
    pear_grade_evaluator = PearGradeEvaluator()
    pear_deterioration_writer = PearDeteriorationWriter()

    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S', level=logging.DEBUG)

    for directory in directories:
        logging.info('target pear: {} started'.format(directory))
        pear = Loader.load_pear(image_root_dir + directory)
        start_time = time.time()

        pear = pear_deterioration_detector.call(pear)

        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info("Deterioration Detect & Classification for {}: {:.2f} [sec]".format(directory, elapsed_time))

        pear = pear_grade_evaluator.call(pear)
        pear_deterioration_writer.call(pear)

        logging.info('target pear: {} end'.format(directory))
        del pear


if __name__ == '__main__':
    load_dotenv()
    main()
