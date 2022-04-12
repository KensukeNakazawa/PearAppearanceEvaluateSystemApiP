""" -*- coding: utf-8
洋ナシの画像の一枚
"""
import os
from typing import List

from numpy import ndarray
from src.pear_domain.value_object.deterioration import Deterioration
from src.pear_domain.value_object.coordinate import Coordinate


class SideOfPear:

    def __init__(
            self,
            image: ndarray,
            side_of_pear_id: int = None,
            area: float = None,
            deteriorations: List[Deterioration] = [],
            contours=None,
            coordinate: Coordinate = None,
            file_path: str = None,
            labeled_image: ndarray = None
    ):
        self.__image = image
        self.__side_of_pear_id = side_of_pear_id
        self.__area = area
        self.__deteriorations = deteriorations
        self.__contours = contours
        self.__coordinate = coordinate
        self.__file_path = file_path
        self.__labeled_image = labeled_image

    @property
    def image(self):
        pass

    @property
    def side_of_pear_id(self):
        pass


    @property
    def area(self):
        pass

    @property
    def deteriorations(self):
        pass

    @property
    def contours(self):
        pass

    @property
    def coordinate(self):
        """洋ナシの輪郭が入る様に設定された座標"""
        pass

    @property
    def file_path(self):
        pass

    @property
    def labeled_image(self):
        pass

    @side_of_pear_id.getter
    def side_of_pear_id(self):
        return self.__side_of_pear_id

    @image.getter
    def image(self) -> ndarray:
        return self.__image

    @area.getter
    def area(self) -> float:
        return self.__area

    @deteriorations.getter
    def deteriorations(self) -> List[Deterioration]:
        return self.__deteriorations

    @contours.getter
    def contours(self) -> ndarray:
        return self.__contours

    @coordinate.getter
    def coordinate(self) -> Coordinate:
        return self.__coordinate

    @file_path.getter
    def file_path(self) -> str:
        return self.__file_path

    @labeled_image.getter
    def labeled_image(self) -> ndarray:
        return self.__labeled_image

    @side_of_pear_id.setter
    def side_of_pear_id(self, side_of_pear_id: int = None):
        if side_of_pear_id is None:
            raise ValueError('side_of_pear_id must not be None')
        if type(side_of_pear_id) is not int:
            raise TypeError('side_of_pear_id must be int type')
        self.__side_of_pear_id = side_of_pear_id
        return None

    @area.setter
    def area(self, area: float):
        if area is None:
            raise ValueError('area must not be None')
        if type(area) is not float:
            raise TypeError('area must be float type')
        self.__area = area
        return None

    @contours.setter
    def contours(self, contours: ndarray) -> None:
        if contours is None:
            raise ValueError('contours must not be None')
        if type(contours) is not ndarray:
            raise TypeError('contours must be ndarray type')
        self.__contours = contours
        return None

    @coordinate.setter
    def coordinate(self, coordinate: Coordinate) -> None:
        if coordinate is None:
            raise ValueError('coordinate must be None')
        if type(coordinate) is not Coordinate:
            raise TypeError('coordinate must be Coordinate type')
        self.__coordinate = coordinate
        return None

    @file_path.setter
    def file_path(self, file_path: str) -> None:
        if type(file_path) is not str:
            raise TypeError('file_path must be string type')
        self.__file_path = file_path
        return None

    @labeled_image.setter
    def labeled_image(self, image: ndarray = None) -> None:
        if image is None:
            raise ValueError('image must be None')
        if type(image) is not ndarray:
            raise TypeError('image must be ndarray type')
        self.__labeled_image = image
        return None

    def get_file_name(self) -> str:
        return os.path.basename(self.file_path)

    def get_dir_name(self) -> str:
        dir_name = os.path.dirname(self.file_path).split('\\')[-1]
        return dir_name.split('/')[-1]

    def calculate_area_rate(self, coordinate: Coordinate) -> float:
        """対象の座標がオブジェクトの中で占める面積の割合を計算する
        Args:
            coordinate(Coordinate): 対象の座標
        Returns:
            area_rate(float): 面積の割合
        """
        area_rate = coordinate.pixel * 0.65 / self.area
        return area_rate

    def add_deterioration(self, deterioration: Deterioration):
        """汚損オブジェクトを追加する
        Args:
            deterioration(Deterioration): 追加する汚損オブジェクト
        Returns:
        """
        if type(deterioration) is not Deterioration:
            raise TypeError('deterioration must be type of Deterioration')
        self.__deteriorations.append(deterioration)
        return None
