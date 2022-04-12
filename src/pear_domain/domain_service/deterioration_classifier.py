# -*- coding: utf-8 -*-
import os

import cv2
import numpy as np
from numpy import ndarray

from tensorflow.keras.models import load_model

from config import constants
from src.pear_domain.entity.pear import Pear


class DeteriorationClassifier:

    def __init__(self):
        self.model_path: str = constants.CNN_MODEL_PATH
        self.model = self.__get_model()
        self.image_size: tuple = (constants.CNN_INPUT_SIZE, constants.CNN_INPUT_SIZE)

    def call(self, pear: Pear):
        return self.__deterioration_classifier(pear)

    def __deterioration_classifier(self, pear: Pear):
        for side_of_pear in pear.side_of_pears:
            for deterioration in side_of_pear.deteriorations:
                target_image = side_of_pear.image[
                    deterioration.coordinate.top: deterioration.coordinate.under,
                    deterioration.coordinate.left: deterioration.coordinate.right
                ]
                predict_class = self.__predict(target_image)
                deterioration_code = self.__convert_deterioration_code(predict_class)
                deterioration.deterioration_code = deterioration_code

    def __predict(self, x: ndarray) -> int:
        if os.environ['ENVIRONMENT'] == 'test':
            import random
            return random.choice(constants.DETERIORATION_CLASSES)
        x: ndarray = self.__preprocess(x)
        x = np.expand_dims(x, 0)
        predictions = self.model.predict(x)
        return int(np.argmax(predictions[0]))

    def __get_model(self):
        """
        学習済みモデルを取得する
        Returns:
            model: 学習済みモデル

        """
        if os.environ["ENVIRONMENT"] == 'test':
            return None
        model = load_model(self.model_path)
        return model

    def __preprocess(self, target_image: ndarray) -> ndarray:
        preprocessed_image = self.__resize_image(target_image)
        preprocessed_image = preprocessed_image.astype('float32') / 255.0
        return preprocessed_image

    def __resize_image(self, target_image: ndarray) -> ndarray:
        """
        画像をリサイズする
        Args:
            target_image(ndarray): リサイズしたい画像

        Returns:
            resized_image(ndarray): リサイズした画像

        """
        resized_image: ndarray = cv2.resize(target_image, self.image_size)
        return resized_image

    @staticmethod
    def __convert_deterioration_code(class_index: int) -> str:
        return constants.DETERIORATION_CLASS_DICTIONARY[class_index]

