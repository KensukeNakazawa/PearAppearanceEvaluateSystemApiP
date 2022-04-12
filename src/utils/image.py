
from datetime import datetime, timedelta, timezone
import os

from boto3.session import Session
import cv2
from numpy import ndarray


def load_from_s3(image_path: str):
    if os.getenv('ENVIRONMENT') == 'local':
        local_image_path = '/var/www/images/original_images/01/Img00016.bmp'
        image = cv2.imread(local_image_path, cv2.IMREAD_COLOR)
    else:
        session = Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name="ap-northeast-1"
        )
        s3 = session.resource('s3')
        aws_bucket_name = os.getenv('AWS_BUCKET_NAME')
        tmp_file_path = './tmp/pear_images/test.png'
        s3.meta.client.download_file(aws_bucket_name, image_path, tmp_file_path)
        image = cv2.imread(tmp_file_path, cv2.IMREAD_COLOR)
        os.remove(tmp_file_path)
    return image


def upload_to_s3(pear_id: int, index: int, image: ndarray, evaluate_flg: bool = False) -> str:
    """一度ローカルに保存してからS3にアップロードする
    See Also:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_file
    Args:
        pear_id:
        index:
        image:
        evaluate_flg:

    Returns:

    """
    jst = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(jst).strftime('%Y%m%d%H%M')
    file_name = '{index}_{now}.png'.format(index=index, now=now)

    # 一時的にローカルにファイルを保存
    local_file_path = './tmp/evaluated_pear_images/' if evaluate_flg else './tmp/pear_images/'
    local_file_path += str(pear_id) + '/'
    if not os.path.exists(local_file_path):
        os.makedirs(local_file_path)
    local_file_name = local_file_path + file_name
    cv2.imwrite(local_file_name, image)

    # ローカルからS3にファイルをアップロード
    if os.getenv('ENVIRONMENT') == 'local':
        s3_file_key = local_file_name
    else:
        s3_file_key = 'evaluated_pear_images/'if evaluate_flg else 'pear_images/'
        s3_file_key += str(pear_id) + '/' + file_name

    if os.getenv('ENVIRONMENT') != 'local':
        session = Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name="ap-northeast-1"
        )
        s3 = session.resource('s3')

        aws_bucket_name = os.getenv('AWS_BUCKET_NAME')
        bucket = s3.Bucket(aws_bucket_name)
        extra_args = {"ACL": "public-read", "ContentType": "image/jpeg"}
        response = bucket.upload_file(local_file_name, s3_file_key, extra_args)

        # 一時的に保存していたファイルを削除
        os.remove(local_file_name)

    return s3_file_key
