""" -*- coding: utf-8 -*-

"""

from src.pear_domain.value_object.coordinate import Coordinate
from config.constants import DETERIORATION_CLASSES


class Deterioration:

    def __init__(self, deterioration_code: str = None,
                 area_rate: float = None,
                 deterioration_class: int = None,
                 coordinate: Coordinate = None):
        self.__pear_deterioration_id = None
        self.__deterioration_code = deterioration_code
        self.__area_rate = area_rate
        self.__deterioration_class = deterioration_class
        self.__coordinate = coordinate

    @property
    def pear_deterioration_id(self):
        pass

    @property
    def deterioration_code(self):
        pass

    @property
    def area_rate(self):
        pass

    @property
    def deterioration_class(self):
        pass

    @property
    def coordinate(self):
        pass

    @pear_deterioration_id.getter
    def pear_deterioration_id(self):
        return self.__pear_deterioration_id

    @deterioration_code.getter
    def deterioration_code(self) -> str:
        return self.__deterioration_code

    @area_rate.getter
    def area_rate(self) -> float:
        return self.__area_rate

    @deterioration_class.getter
    def deterioration_class(self):
        return self.__deterioration_class

    @coordinate.getter
    def coordinate(self):
        return self.__coordinate

    @pear_deterioration_id.setter
    def pear_deterioration_id(self, pear_deterioration_id: int = None) -> None:
        if pear_deterioration_id is None:
            raise ValueError('pear_deterioration_id must not be None')
        if type(pear_deterioration_id) is not int:
            raise TypeError('pear_deterioration_id must be int type')
        self.__pear_deterioration_id = pear_deterioration_id
        return None

    @deterioration_code.setter
    def deterioration_code(self, deterioration_code: str = None):
        if deterioration_code is None:
            raise ValueError('deterioration_code must not be None')
        if type(deterioration_code) is not str:
            raise TypeError('deterioration_code must be str type')
        self.__deterioration_code = deterioration_code
        return None

    @area_rate.setter
    def area_rate(self, area_rate: float):
        if area_rate is None:
            raise ValueError('area_rate must not be None')
        if type(area_rate) is not float:
            raise TypeError('area_rate must be float type')
        self.__area_rate = area_rate
        return None

    @deterioration_class.setter
    def deterioration_class(self, deterioration_class: int):
        if deterioration_class is None:
            raise ValueError('deterioration_class must not be None')

        if type(deterioration_class) is not int:
            raise TypeError('deterioration_class must be int type')

        if deterioration_class not in DETERIORATION_CLASSES:
            raise ValueError('deterioration class must  be in {}'.format(DETERIORATION_CLASSES))
        self.__deterioration_class = deterioration_class
        return None

    @coordinate.setter
    def coordinate(self, coordinate: Coordinate):
        if coordinate is None:
            raise ValueError('coordinate must not be None')
        if type(coordinate) is not Coordinate:
            raise TypeError('coordinate must be type of Coordinate')
        self.__coordinate = coordinate
        return None
