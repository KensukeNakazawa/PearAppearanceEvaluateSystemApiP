# -*-coding: utf-8
import os
import pickle
from typing import Tuple

import cv2
import numpy as np
from numpy import ndarray
import pandas as pd
import xgboost as xgb

from config import constants
from src.pear_domain.domain_service.glcm_calculator import GLCMCalculator


class DeteriorationEvaluator:
    def __init__(self):
        self.glcm_calculator = GLCMCalculator()
        self.model_glcm = pickle.load(open(constants.DETECTION_MODEL_GLCM_PATH, 'rb'))
        # self.model_hist = pickle.load(open(constants.DETECTION_MODEL_HIST_PATH, 'rb'))

    def call(self, target_image: ndarray) -> bool:
        """対象の画像が汚損画像かどうかを判定する
        時間のかかる処理のため，テスト環境ではランダムでboolを返す
        Args:
            target_image(ndarray): 対象の画像
        Returns:
            is_deterioration(bool): 汚損かどうか，汚損であればTrue
        """
        if os.getenv('ENVIRONMENT') == 'test':
            import random
            return random.choice([True, False])
        return self.__deterioration_detect(target_image)

    def __deterioration_detect(self, image: ndarray) -> bool:
        """汚損ブロック判定の本体
        Args:
            image:
        Returns:
        """
        is_deterioration_glcm: bool = self.__deterioration_with_glcm_random_forest(image)
        # is_deterioration_hist: bool = self.__deterioration_with_hist_random_forest(image)

        return is_deterioration_glcm

    def __deterioration_with_hist_random_forest(self, image: ndarray) -> bool:
        """ヒストグラムを基にランダムフォレストを用いて汚損かどうかを判定する
        Args:
            image(ndarray):
        Returns:
            result(bool): 判定結果
        """
        hist_r, hist_g, hist_b = self.__calc_hist(image)
        x = [np.ravel(hist_r + hist_g + hist_b)]
        predictions = self.model_hist.predict(x)
        return True if predictions[0] == 3 else False

    def __deterioration_with_glcm_random_forest(self, image: ndarray) -> bool:
        target_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        img_h, img_l, img_s = target_image[:, :, 0], target_image[:, :, 1], target_image[:, :, 2]
        texture_feature = self.glcm_calculator.call(img_h)
        predictions = self.model_glcm.predict([texture_feature])
        return True if predictions[0] == 3 else False

    def __detection_with_xgboost(self, image: ndarray) -> bool:
        """
        Args:
            image:

        Returns:
            result(bool): 判定結果
        """
        target_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        img_h, img_l, img_s = target_image[:, :, 0], target_image[:, :, 1], target_image[:, :, 2]
        texture_feature = self.glcm_calculator.call(img_h)
        texture_feature = pd.DataFrame(texture_feature).T
        texture_feature.columns = constants.FEATURE_NAMES
        input_feature = xgb.DMatrix(texture_feature)
        predictions = self.model_glcm.predict(input_feature)
        return True if predictions[0] == 2 else False

    @staticmethod
    def __calc_hist(image: ndarray) -> Tuple[ndarray, ndarray, ndarray]:
        """ヒストグラムを計算する
        Args:
            image:
        Returns:

        """
        b, g, r = image[:, :, 0], image[:, :, 1], image[:, :, 2]
        hist_b = cv2.calcHist([b], [0], None, [constants.HIST_SIZE], [0, 256])
        hist_g = cv2.calcHist([g], [0], None, [constants.HIST_SIZE], [0, 256])
        hist_r = cv2.calcHist([r], [0], None, [constants.HIST_SIZE], [0, 256])
        return hist_r, hist_g, hist_b
