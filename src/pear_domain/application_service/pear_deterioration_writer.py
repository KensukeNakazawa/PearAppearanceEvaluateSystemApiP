# -*- coding: utf-8 -*-
import os
from copy import copy
from typing import Tuple

import cv2
from numpy import ndarray

from config.constants import DETERIORATION_CLASS_DICTIONARY

from src.pear_domain.repository.deterioration_repository import DeteriorationRepository
from src.pear_domain.value_object.deterioration import Deterioration
from src.pear_domain.entity.pear import Pear


class PearDeteriorationWriter:
    def __init__(self):
        self.deterioration_repository = DeteriorationRepository()

    def call(self, pear: Pear):
        for side_of_pear in pear.side_of_pears:
            target_image = copy(side_of_pear.image)
            for deterioration in side_of_pear.deteriorations:
                target_image = self.__labeling(target_image, deterioration)
            side_of_pear.labeled_image = target_image

    def __labeling(self, image: ndarray, deterioration: Deterioration) -> ndarray:
        """
        ラベルをつける対象の画像に対して，バウンディングボックスの作成及びラベルの文字付与を行う
        Args:
            image(ndarray): 対象の画像
            deterioration(Deterioration): 汚損のオブジェクト
        Returns:
            labeled_image(ndarray): 対象画像にバウンディングﾎボックス及びラベルをつけた後の画像
        """
        # ラベル付けの対象位置を定義
        coordinate = deterioration.coordinate
        upper_left: tuple = (coordinate.left, coordinate.top)
        under_right: tuple = (coordinate.right, coordinate.under)

        pure_deterioration = self.deterioration_repository.find_by_deterioration_code(deterioration.deterioration_code)
        deterioration.pear_deterioration_id = pure_deterioration.deterioration_id
        deterioration.pear_deterioration_id = pure_deterioration.deterioration_id

        bbox_label = pure_deterioration.deterioration_name + '({:.2f}%)'.format(deterioration.area_rate * 100)
        bbox_color = pure_deterioration.get_color_bgr()

        # ラベル付け対象の位置にバウンディングボックスを生成
        labeled_image = cv2.rectangle(image, upper_left, under_right, color=bbox_color, thickness=10)
        # バウンディングボックスに対してラベルの文字を付与
        labeled_image = cv2.putText(
            labeled_image,
            bbox_label,
            (coordinate.left, int(coordinate.top - 5)),
            cv2.FONT_HERSHEY_COMPLEX,
            1.5,
            bbox_color,
            3
        )
        return labeled_image
