# -*- coding: utf-8 -*-
import logging
import os
from optparse import OptionParser
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from dotenv import load_dotenv

from src.pear_domain.domain_service.loader import Loader

from src.pear_domain.application_service.pear_deterioration_detector import PearDeteriorationDetector
from src.pear_domain.application_service.pear_grade_evaluator import PearGradeEvaluator
from src.pear_domain.application_service.pear_deterioration_writer import PearDeteriorationWriter


def main():
    directory = get_dir_from_arg()

    logging.info('target pear: {} started'.format(directory))

    execute_evaluate_system(directory)

    logging.info('target pear: {} end'.format(directory))


def get_dir_from_arg():
    parser = OptionParser()
    parser.add_option('-d', '--directory_name',
                      type='string',
                      help="Directory Full Path")
    (options, args) = parser.parse_args()
    directory = options.directory_name

    if not os.path.exists(directory):
        raise NotADirectoryError('argment directory not found')

    return directory


def execute_evaluate_system(directory: str):
    pear_deterioration_detector = PearDeteriorationDetector()
    pear_grade_evaluator = PearGradeEvaluator()
    pear_deterioration_writer = PearDeteriorationWriter()

    pear = Loader.load_pear(directory)

    start_time = time.time()

    pear = pear_deterioration_detector.call(pear)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info("Deterioration Detect & Classification for {}: {:.2f} [sec]".format(directory, elapsed_time))

    pear = pear_grade_evaluator.call(pear)
    pear_deterioration_writer.call(pear)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S', level=logging.DEBUG)
    load_dotenv()
    main()
