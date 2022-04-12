"""　-*- coding utf-8 -*-
"""


class Coordinate:
    """

    """

    def __init__(self, under: int, top: int, left: int, right: int, pixel: int = None) -> None:
        self.__under: int = under
        self.__top: int = top
        self.__left: int = left
        self.__right: int = right
        self.__pixel: float = pixel

    @property
    def under(self):
        pass

    @property
    def top(self):
        pass

    @property
    def left(self):
        pass

    @property
    def right(self):
        pass

    @property
    def pixel(self):
        pass

    @under.getter
    def under(self) -> int:
        return self.__under

    @top.getter
    def top(self) -> int:
        return self.__top

    @left.getter
    def left(self) -> int:
        return self.__left

    @right.getter
    def right(self) -> int:
        return self.__right

    @pixel.getter
    def pixel(self) -> float:
        return self.__pixel

    @under.setter
    def under(self, under: int) -> None:
        if under is None:
            raise ValueError('under must not be None')
        if type(under) is not int:
            raise TypeError('under must be int type')
        self.__under = under
        return None

    @top.setter
    def top(self, top: int) -> None:
        if top is None:
            raise ValueError('top must not be None')
        if type(top) is not int:
            raise TypeError('top must be int type')
        self.__top = top
        return None

    @left.setter
    def left(self, left: int) -> None:
        if left is None:
            raise ValueError('left must not be None')
        if type(left) is not int:
            raise TypeError('left must be float type')
        self.__left = left
        return None

    @right.setter
    def right(self, right: int) -> None:
        if right is None:
            raise ValueError('right must not be None')
        if type(right) is not int:
            raise TypeError('right must be int type')
        self.__right = right
        return None

    @pixel.setter
    def pixel(self, pixel: int) -> None:
        if pixel is None:
            raise ValueError('pixel must not be None')
        if type(pixel) is not float:
            raise TypeError('pixel must be int float')
        self.__pixel = pixel
        return None
