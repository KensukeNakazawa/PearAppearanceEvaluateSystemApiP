# coding: utf-8

import cv2

from config import constants
from src.pear_domain.value_object.coordinate import Coordinate
from src.pear_domain.entity.side_of_pear import SideOfPear
from src.repositories.abstract_image_repository import AbstractImageRepository


class BlockImageRepository(AbstractImageRepository):

    @classmethod
    def save_image(cls, side_of_pear: SideOfPear, target_coordinate: Coordinate, is_deterioration: bool) -> None:
        if not constants.SAVE_BLOCK_IMAGE_FLG:
            return None

        save_dir_name = constants.SAVE_BLOCK_IMAGE_PATH + '/' + str(int(is_deterioration))
        super().make_directory(dir_name=save_dir_name)

        save_file_name = save_dir_name + '/' + cls.__convert_file_name(target_coordinate) + side_of_pear.get_file_name()

        block_image = side_of_pear.image[
                      target_coordinate.top: target_coordinate.under,
                      target_coordinate.left: target_coordinate.right
                      ]
        cv2.imwrite(save_file_name, block_image)
        return None

    @staticmethod
    def __convert_file_name(coordinate: Coordinate) -> str:
        return str(coordinate.left) \
               + '_' \
               + str(coordinate.right) \
               + '_' \
               + str(coordinate.top) \
               + '_' \
               + str(coordinate.under) \
               + '_'
