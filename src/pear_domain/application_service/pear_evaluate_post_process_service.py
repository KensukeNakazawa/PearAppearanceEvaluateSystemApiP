
from src.utils.image import upload_to_s3
from src.pear_domain.repository.pear_repository import PearRepository


class PearEvaluatePostProcessService:
    def __init__(self):
        self.pear_repository = PearRepository()

    def end_evaluate(self, pear):
        # 評価済みの画像をS3にアップする
        s3_file_keys = []
        for index, side_of_pear in enumerate(pear.side_of_pears):
            s3_file_key = upload_to_s3(pear.pear_id, index=index, image=side_of_pear.labeled_image, evaluate_flg=True)
            s3_file_keys.append(s3_file_key)
        self.pear_repository.save_pear_at_evaluated(pear, s3_file_keys)
