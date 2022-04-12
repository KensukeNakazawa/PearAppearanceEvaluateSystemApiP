# -*- coding: utf-8 -*-

from typing import List

import numpy as np
from numpy import ndarray
from skimage.feature.texture import greycomatrix
from skimage.feature.texture import greycoprops

from config import constants


class GLCMCalculator:
    """
     details: https://scikit-image.org/docs/dev/api/skimage.feature.html#greycomatrix:title
    """

    def __init__(self, levels: int = 181, symmetric: bool = True, normed: bool = True):
        """
        初期化
        detail: https://scikit-image.org/docs/dev/api/skimage.feature.html#skimage.feature.greycomatrix
        Args:
            levels:
            symmetric:
            normed:
        """
        self.distances: list = constants.DISTANCES
        self.angles: list = constants.ANGLES
        self.levels: int = levels
        self.symmetric: bool = symmetric
        self.normed: bool = normed
        self.feature_names = constants.FEATURE_NAMES

    def call(self, image: ndarray) -> List[float]:
        return self.__calc_texture_features(image)

    def __calc_texture_features(self, image: ndarray) -> List[float]:
        """
        GLCMを計算し，テクスチャ特徴量を計算する
        details: https://scikit-image.org/docs/dev/api/skimage.feature.html#skimage.feature.greycoprops
        https://github.com/scikit-image/scikit-image/blob/372b901065d5712237105fb1a70c5c6cde530a15/skimage/feature/texture.py#L157
        Args:
            image: テクスチャ特徴量を計算したい対象の画像
        Returns:
            texture_feature(List[float]): 各テクスチャ特徴量に対して計算したリスト
        """
        texture_features = []
        for feature_name in self.feature_names:
            try:
                glcm = self.__calc_glcm(image)
                features = greycoprops(glcm, feature_name)
                texture_features.append(float(np.mean(features)))
            except Exception as e:
                print(np.max(image))
                print(e)
        return texture_features

    def __calc_glcm(self, image: ndarray) -> list:
        """
        グレーレベル共起行列の計算
        details: https://scikit-image.org/docs/dev/api/skimage.feature.html#skimage.feature.greycomatrix
        Args:
            image: 同時生成行列を計算したい対象の画像
        Returns:
            glcm: 計算された同時生成行列
        """
        return greycomatrix(image, self.distances, self.angles, self.levels, self.symmetric, self.normed)
