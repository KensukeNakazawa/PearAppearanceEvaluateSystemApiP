""" -*- coding: utf-8
汚損の検出処理を行う
"""
from typing import Dict

import cv2
import numpy as np
from numpy import ndarray

from config import constants

from src.pear_domain.domain_service.deterioration_evaluator import DeteriorationEvaluator
from src.pear_domain.value_object.coordinate import Coordinate
from src.pear_domain.value_object.deterioration import Deterioration
from src.pear_domain.entity.pear import Pear
from src.pear_domain.entity.side_of_pear import SideOfPear
from src.repositories.binary_image_repository import BinaryImageRepository
from src.repositories.block_image_repository import BlockImageRepository


class LabelingProcessor:

    def __init__(self):
        self.__block_size: int = constants.BLOCK_SIZE
        self.__level_in_contours = {
            1: 'all out of contour',
            2: 'partially  within contours',
            3: 'all within contours'
        }
        self.__deterioration_evaluator = DeteriorationEvaluator()

    @property
    def block_size(self):
        pass

    @property
    def level_in_contours(self):
        pass

    @property
    def deterioration_evaluator(self):
        pass

    @block_size.getter
    def block_size(self):
        return self.__block_size

    @level_in_contours.getter
    def level_in_contours(self):
        return self.__level_in_contours

    @deterioration_evaluator.getter
    def deterioration_evaluator(self):
        return self.__deterioration_evaluator

    def call(self, pear: Pear) -> None:
        if type(pear) is not Pear:
            raise TypeError('this parameter(pear) must be type of Pear')
        self.__labeling_process(pear)

    def __labeling_process(self, pear: Pear):
        """
        Args:
            pear:

        Returns:

        """
        for side_of_pear in pear.side_of_pears:
            self.__labeling_process_for_side(side_of_pear)
        return None

    def __labeling_process_for_side(self, side_of_pear: SideOfPear) -> None:
        """汚損の検出，ラベリング処理を行う
        Args:
            side_of_pear(SideOfPear):
        Returns:
        """
        coordinate = side_of_pear.coordinate
        block_nums = self.__calculate_block_num(coordinate)

        # 入力画像と同じサイズの画素値0の画像を想定したオブジェクト
        binary_image: ndarray = np.zeros(side_of_pear.image.shape).astype(side_of_pear.image.dtype)

        for i in range(0, block_nums['column']):
            column_start = (i * self.block_size) + coordinate.left
            column_end = column_start + self.block_size
            for j in range(0, block_nums['row']):
                row_start = (j * self.block_size) + coordinate.top
                row_end = row_start + self.block_size

                target_coordinate = Coordinate(under=row_end, top=row_start, left=column_start, right=column_end)
                result_level_in_contours = self.__check_image_in_contours(target_coordinate, side_of_pear)

                is_deterioration = self.__check_deterioration(side_of_pear, target_coordinate, result_level_in_contours)

                color = 255 if is_deterioration else 0
                binary_image: ndarray = self.__fill_image(binary_image, target_coordinate, color)
        binary_image: ndarray = cv2.cvtColor(binary_image, cv2.COLOR_BGR2GRAY)
        self.__labeling(side_of_pear, binary_image)

        return None

    def __calculate_block_num(self, coordinate: Coordinate) -> Dict[str, int]:
        """
        洋ナシの座標からブロック化した際のブロック数を計算する．
        Args:
            coordinate(Coordinate): 洋ナシの座標
        Returns:
            block_num(Dict[str, int]): ブロック化した際の縦横の長さ
        """
        # 背景を除去した後の縦と横の長さを計算
        column_length = coordinate.right - coordinate.left
        row_length = coordinate.under - coordinate.top
        column_block_num = int(column_length / self.block_size)
        row_block_num = int(row_length / self.block_size)

        return {'column': column_block_num, 'row': row_block_num}

    @staticmethod
    def __check_image_in_contours(target_coordinate: Coordinate, side_of_pear: SideOfPear) -> int:
        """
          対象のブロック画像が，洋ナシの輪郭の中に入っているかをチェックする．
          See https://docs.opencv.org/4.5.3/d3/dc0/group__imgproc__shape.html#ga1a539e8db2135af2566103705d7a5722
          Args:
              target_coordinate(Coordinate): 対象のブロックの座標
              side_of_pear(SideOfPear): 洋ナシの横方向のオブジェクト
          Returns:
              result(int): 輪郭に入っているかどうかのパターン
              example:
                  pattern1. 全て輪郭外
                  pattern2. 一部輪郭内
                  pattern3. 全て輪郭内
        """
        point = 0
        measure_dist = False

        contours = side_of_pear.contours
        # 左上が輪郭内かどうか
        if cv2.pointPolygonTest(contours, (target_coordinate.top, target_coordinate.left), measure_dist) >= 0:
            point += 1
        # 左下が輪郭内かどうか
        if cv2.pointPolygonTest(contours, (target_coordinate.under, target_coordinate.left), measure_dist) >= 0:
            point += 1
        # 右上が輪郭内かどうか
        if cv2.pointPolygonTest(contours, (target_coordinate.top, target_coordinate.right), measure_dist) >= 0:
            point += 1
        # 右下が輪郭内かどうか
        if cv2.pointPolygonTest(contours, (target_coordinate.under, target_coordinate.right), measure_dist) >= 0:
            point += 1

        if point == 0:
            result = 1
        elif point == 4:
            result = 3
        else:
            result = 2

        return result

    def __check_deterioration(self, side_of_pear: SideOfPear, target_coordinate: Coordinate, level_in_contours: int) -> bool:
        """
        Args:
            side_of_pear(SideOfPear):
            target_coordinate(Coordinate):
            level_in_contours(int):
        Returns:
            is_deterioration(bool): 汚損ブロックかどうか
        """
        block_image = side_of_pear.image[
            target_coordinate.top: target_coordinate.under,
            target_coordinate.left: target_coordinate.right
        ]

        is_deterioration = False
        if level_in_contours == 3:
            is_deterioration = self.__deterioration_evaluator.call(block_image)
            BlockImageRepository.save_image(side_of_pear, target_coordinate, is_deterioration)

        return is_deterioration

    @staticmethod
    def __fill_image(image: ndarray, coordinate: Coordinate, color: int) -> ndarray:
        """
        画像の対象領域を指定の色で塗潰す．
        Args:
            image(ndarray): 対象画像
            coordinate(Coordinate): 対象の座標
            color(int): 指定の色
        Returns:
            filled_image(ndarray): 塗潰した画像
        """
        filled_image = cv2.rectangle(
            image,
            (coordinate.left, coordinate.top),
            (coordinate.right, coordinate.under),
            color,
            cv2.FILLED
        )
        return filled_image

    @staticmethod
    def __labeling(side_of_pear: SideOfPear, binary_image: ndarray):
        """
        与えられたバイナリの画像に対してラベリング処理を行う．
        Args:
            binary_image(ndarray): バイナリ画像
        """
        # label_num -> ラベリングされたラベルの数
        # stats -> 各ラベルの情報(cv::ConnectedComponentsTypes)
        #   @see: https://docs.opencv.org/4.5.3/d3/dc0/group__imgproc__shape.html#gac7099124c0390051c6970a987e7dc5c5)
        #   ex) 0: 左上のX座標，1: 左上のY座標, 2: 幅, 3: 高さ, 4: 面積
        # 8近傍処理(connectivity=8)
        label_num, _, stats, _ = cv2.connectedComponentsWithStats(
            image=binary_image,
            connectivity=constants.LABELING_CONNECTIVITY
        )
        # ラベルが0，すなわち背景を除く
        target_image_data = np.delete(stats, 0, 0)

        BinaryImageRepository.save_image(side_of_pear, binary_image)

        for index, target_image_datum in enumerate(target_image_data):
            left, top, width, height, area = target_image_datum

            if area > 40:
                right: int = left + width
                under: int = top + height

                # 該当の画像の中での汚損のピクセル数を算出する
                target_image = binary_image[top: under, left: right]
                pixel_num = cv2.countNonZero(target_image)

                labeled_coordinate = Coordinate(
                    under=under,
                    top=top,
                    left=left,
                    right=right,
                    pixel=pixel_num
                )
                deterioration = Deterioration(coordinate=labeled_coordinate, deterioration_code=None)
                deterioration.area_rate = side_of_pear.calculate_area_rate(labeled_coordinate)
                side_of_pear.add_deterioration(deterioration)
