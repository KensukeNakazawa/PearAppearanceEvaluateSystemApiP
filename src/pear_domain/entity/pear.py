""" -*- coding: utf-8 -*-
洋ナシのオブジェクト
"""

from typing import List
from src.pear_domain.entity.side_of_pear import SideOfPear


class Pear:

    def __init__(self, pear_id: int = None, side_of_pears: List[SideOfPear] = [], rank_id: int = 0) -> None:
        self.__pear_id = pear_id
        self.__side_of_pears = side_of_pears
        self.__rank_id = rank_id
        self.__max_side_of_pears = 4

    @property
    def pear_id(self):
        pass

    @property
    def side_of_pears(self):
        pass

    @property
    def rank_id(self):
        pass

    @property
    def max_side_of_pears(self):
        pass

    @pear_id.getter
    def pear_id(self):
        return self.__pear_id

    @rank_id.getter
    def rank_id(self):
        return self.__rank_id

    @side_of_pears.getter
    def side_of_pears(self) -> List[SideOfPear]:
        return self.__side_of_pears

    @max_side_of_pears.getter
    def max_side_of_pears(self) -> int:
        """

        Returns:

        """
        return self.__max_side_of_pears

    @pear_id.setter
    def pear_id(self, pear_id: int = None) -> None:
        if pear_id is None:
            raise ValueError('pear_id must not be None')
        if type(pear_id) is not int:
            raise TypeError('pear_id must be int')
        self.__pear_id = pear_id
        return None

    @rank_id.setter
    def rank_id(self, rank_id: int = None):
        if rank_id is None:
            raise ValueError('score must not be None')
        if type(rank_id) is not int:
            raise TypeError('score must be int')
        self.__rank_id = rank_id
        return None

    def add_side_of_pear(self, side_of_pear: SideOfPear):
        """"""
        if not isinstance(side_of_pear, SideOfPear):
            raise TypeError('part_of_pear must be PartOfPear type')
        if len(self.side_of_pears) >= self.max_side_of_pears:
            raise ValueError('number of part_of_pear must be under {}'.format(self.max_side_of_pears))
        self.__side_of_pears.append(side_of_pear)
        return None
