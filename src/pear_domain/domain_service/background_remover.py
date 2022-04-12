# -*- coding: utf-8 -*-

from numpy import ndarray
import numpy as np
import cv2

from config import constants
from src.pear_domain.value_object.coordinate import Coordinate
from src.pear_domain.entity.pear import Pear
from src.pear_domain.entity.side_of_pear import SideOfPear


class BackgroundRemover:
    """

    """

    def __init__(self):
        self.block_size = constants.BLOCK_SIZE

    def call(self, pear: Pear):
        if type(pear) is not Pear:
            raise TypeError('this parameter(pear) must be type of Pear')
        self.__remove_background(pear)

    def __remove_background(self, pear: Pear):
        for side_of_pear in pear.side_of_pears:
            self.__set_pear_contours(side_of_pear)
            self.__set_pear_coordinate(side_of_pear)
        self.__set_pear_area(pear)

    def __set_pear_contours(self, side_of_pear: SideOfPear) -> None:
        """洋ナシの側面に対して, 輪郭を検出し，輪郭の情報をセットする
        see https://docs.opencv.org/4.5.3/d3/dc0/group__imgproc__shape.html#ga2c759ed9f497d4a618048a2f56dc97f1
        Args:
            side_of_pear(SideOfPear): 洋ナシの側面
        """
        target_image = side_of_pear.image

        image_binary = self.__binarization_image(target_image)
        pear_contours = self.__get_contours(image_binary)

        side_of_pear.contours = pear_contours

        return None

    @staticmethod
    def __set_pear_area(pear: Pear) -> None:
        """輪郭から面積を計算して，面積をセットする
        Args:
            side_of_pear:
        Returns:
        """
        contour_area = 0
        for side_of_pear in pear.side_of_pears:
            contour_area += cv2.contourArea(side_of_pear.contours)
            
        for side_of_pear in pear.side_of_pears:            
            side_of_pear.area = contour_area

    def __set_pear_coordinate(self, side_of_pear: SideOfPear) -> None:
        """洋ナシの側面の輪郭を含む，座標の情報をセットする
        Args:
            side_of_pear:

        Returns:
        """
        # 輪郭の集合から，バウンディングボックスの情報を取得する
        # see https://docs.opencv.org/4.5.3/d3/dc0/group__imgproc__shape.html#ga103fcbda2f540f3ef1c042d6a9b35ac7
        x_min, y_min, width, height = cv2.boundingRect(side_of_pear.contours)

        y_max: int = y_min + height
        x_max: int = x_min + width

        y_length: int = y_max - y_min
        x_length: int = x_max - x_min

        row_lack = self.__calculate_rack_pixel(y_length)
        column_lack = self.__calculate_rack_pixel(x_length)

        row_lacks = [(row_lack + i) // 2 for i in range(2)]
        column_lacks = [(column_lack + i) // 2 for i in range(2)]

        coordinate = Coordinate(
            under=(y_max + row_lacks[0]),
            top=(y_min + row_lacks[1]),
            left=(x_min + column_lacks[0]),
            right=(x_max + column_lacks[1])
        )

        side_of_pear.coordinate = coordinate
        return None

    @staticmethod
    def __binarization_image(target_image: ndarray) -> ndarray:
        """画像を2値化する
        Args:
            target_image(ndarray): 対象の画像
        Returns:
            image_binary(ndarray): 2値化された画像
        """
        image_blur = cv2.GaussianBlur(target_image, (19, 19), 0)
        # BGR -> HLSの変換をし，彩度(S)を取得する
        image_saturation = cv2.cvtColor(image_blur, cv2.COLOR_BGR2HLS)[:, :, 2].astype(np.uint8)
        # 大津の2値化の2値化を行う
        # @see https://docs.opencv.org/4.5.3/d7/d1b/group__imgproc__misc.html#gae8a4a146d1ca78c626a53577199e9c57
        _, image_binary = cv2.threshold(image_saturation, 0, 255, cv2.THRESH_OTSU)

        return image_binary

    @staticmethod
    def __get_contours(image_binary: ndarray):
        """2値化された画像から輪郭を検出する
        see https://docs.opencv.org/4.5.3/d3/dc0/group__imgproc__shape.html#gadf1ad6a0b82947fa1fe3c3d497f260e0
        Args:
            image_binary(ndarray): 2値化画像
        Returns:

        """
        contours, hierarchy = cv2.findContours(
            image=image_binary,
            mode=cv2.RETR_EXTERNAL,
            method=cv2.CHAIN_APPROX_SIMPLE
        )
        # 一番大きい輪郭を抽出
        max_contours = max(contours, key=lambda x: cv2.contourArea(x))
        return max_contours

    def __calculate_rack_pixel(self, target_length):
        """そのままブロック分割すると小ブロックのサイズが壊れてしまうかもしれないので，画像の面積をブロックサイズの公倍数にする
        Args:
            target_length(int):
        Returns:
            rack_pixel(int): 少ブロックを作成する時に分割ができるように公倍数にするための，足りないピクセル
        """
        block_pixel: int = self.block_size

        rack_pixel: int = int(block_pixel * round(target_length / block_pixel)) - target_length
        return rack_pixel
