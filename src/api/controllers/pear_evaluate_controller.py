#
from src.api.requests.pear_evaluate_request import PearEvaluateRequest
from src.pear_domain.application_service.pear_evaluate_service import PearEvaluateService


def pear_evaluate():
    pear_evaluate_request = PearEvaluateRequest()
    # # # S3にアップロードする
    pear_evaluate_service = PearEvaluateService()
    response = pear_evaluate_service.pear_evaluate(pear_evaluate_request)

    return response


def get_pear(pear_id: int):
    pear_evaluate_service = PearEvaluateService()
    response = pear_evaluate_service.get_pear(pear_id)

    return response


def get_pear_evaluates():
    pear_evaluate_service = PearEvaluateService()
    response = pear_evaluate_service.get_pear_evaluates()
    return response
