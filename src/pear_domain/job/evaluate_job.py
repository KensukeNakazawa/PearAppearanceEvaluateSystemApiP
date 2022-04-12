import os
import sys

from celery import Celery
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from src.pear_domain.application_service.pear_deterioration_detector import PearDeteriorationDetector
from src.pear_domain.application_service.pear_grade_evaluator import PearGradeEvaluator
from src.pear_domain.application_service.pear_evaluate_post_process_service import PearEvaluatePostProcessService
from src.pear_domain.application_service.pear_deterioration_writer import PearDeteriorationWriter
from src.pear_domain.repository.pear_repository import PearRepository


job = Celery('tasks', broker='redis://redis:6379')

# タスク実行後の結果をredisに格納する
job.conf.result_backend = 'redis://redis:6379/0'

load_dotenv()


@job.task
def evaluate_delay(pear_id: int):

    pear_deterioration_detector = PearDeteriorationDetector()
    pear_grade_evaluator = PearGradeEvaluator()
    pear_deterioration_writer = PearDeteriorationWriter()
    pear_evaluate_post_process_service = PearEvaluatePostProcessService()

    pear_repository = PearRepository()

    print("START EVALUATION!!")
    pear = pear_repository.find_by_id(pear_id)

    pear = pear_deterioration_detector.call(pear)

    pear = pear_grade_evaluator.call(pear)
    pear_deterioration_writer.call(pear)
    print("END EVALUATION!!")

    print("POST PROCESSING START")
    pear_evaluate_post_process_service.end_evaluate(pear)
    print("POST PROCESSING END")
