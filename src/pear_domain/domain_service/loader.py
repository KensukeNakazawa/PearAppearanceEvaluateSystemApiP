""" -*- coding: utf-8
"""
import glob

import cv2
from numpy import ndarray

from config import constants
from src.pear_domain.entity.pear import Pear
from src.pear_domain.entity.side_of_pear import SideOfPear


class Loader:

    @classmethod
    def load_pear(cls, directory_path: str) -> Pear:
        """洋ナシのオブジェクトをロードする

        Args:
            directory_path(str): 対象の洋ナシ画像が含まれるディレクトリ ex) ・・・/AppearanceGradeEvaluation/images/1

        Returns:
            pear(Pear): 洋ナシの各画像をセットした洋ナシオブジェクト
        """
        # この様にしないと前回のインスタンスの影響をなぜか受けてしまったので，初期値を指定している
        pear = Pear(side_of_pears=[], score=0.0)
        files: list = glob.glob(directory_path + "/*." + constants.IMAGE_EXTENSION)
        for file in files:
            image: ndarray = cv2.imread(file, cv2.IMREAD_COLOR)
            side_of_pear = SideOfPear(
                image=image, 
                area=None, 
                deteriorations=[], 
                contours=None, 
                coordinate=None
            )
            side_of_pear.file_path = file
            pear.add_side_of_pear(side_of_pear)
        return pear
