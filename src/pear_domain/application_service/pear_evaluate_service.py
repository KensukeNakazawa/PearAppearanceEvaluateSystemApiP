import os

from src.utils.image import upload_to_s3
from src.api.requests.pear_evaluate_request import PearEvaluateRequest
from src.pear_domain.job.evaluate_job import evaluate_delay

from src.pear_domain.repository.pear_repository import PearRepository
from src.pear_domain.repository.side_of_pear_repository import SideOfPearRepository
from src.pear_domain.repository.deterioration_repository import DeteriorationRepository


class PearEvaluateService:
    def __init__(self):
        self.pear_repository = PearRepository()
        self.side_of_pear_repository = SideOfPearRepository()
        self.deterioration_repository = DeteriorationRepository()

    def pear_evaluate(self, request: PearEvaluateRequest):
        pear_id = self.pear_repository.create()

        s3_file_keys = []
        for index, image in enumerate(request.images):
            s3_file_key = upload_to_s3(pear_id, index, image)
            s3_file_keys.append(s3_file_key)

        self.pear_repository.create_side_of_pear(pear_id, image_paths=s3_file_keys)

        evaluate_delay.delay(pear_id)
        return {
            'message': 'OK',
            'pear_id': pear_id
        }

    def get_pear(self, pear_id: int):
        pear_db = self.pear_repository.get_pear_by_id(pear_id)
        # DN = Done, NY = Not Yet
        evaluate_code = pear_db.rank_name

        side_of_pears = self.side_of_pear_repository.get_side_of_pear_by_pear_id(pear_id)
        evaluated_side_of_pears = self.side_of_pear_repository.get_evaluated_side_of_pear_by_pear_id(pear_id)
        pear_deteriorations = self.deterioration_repository.get_deterioration_by_pear_id(pear_id)

        if os.getenv('ENVIRONMENT') == 'local':
            pear_images = [side_of_pear.image_path for side_of_pear in side_of_pears]
            evaluated_images = [evaluated_side_of_pear.image_path for evaluated_side_of_pear in evaluated_side_of_pears]
        else:
            pear_images = ["https://yamazaki-smart-agri.s3.ap-northeast-1.amazonaws.com/" + side_of_pear.image_path for side_of_pear in side_of_pears]
            evaluated_images = ["https://yamazaki-smart-agri.s3.ap-northeast-1.amazonaws.com/" + evaluated_side_of_pear.image_path for evaluated_side_of_pear in evaluated_side_of_pears]
        deteriorations = [
            {'name': pear_deterioration.name, 'ratio': round(pear_deterioration.ratio * 100, 2)}
            for pear_deterioration in pear_deteriorations
        ]

        return {
            'message': 'OK',
            'evaluate_code': evaluate_code,
            'pear_images': pear_images,
            'evaluated_images': evaluated_images,
            'deteriorations': deteriorations
        }

    def get_pear_evaluates(self):
        pear_db = self.pear_repository.get_all()

        pears = []

        for pear in pear_db:
            pears.append(
                {
                    'pear_id': pear.pear_id,
                    'evaluate_code': pear.rank_name,
                    'start_at': pear.created_at
                }
            )

        return {
            'message': 'OK',
            'pears': pears
        }

