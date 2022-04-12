# -*- coding: utf-8 -*-
import cv2
from numpy import ndarray

from config import constants
from src.pear_domain.entity.side_of_pear import SideOfPear

from src.repositories.abstract_image_repository import AbstractImageRepository


class BinaryImageRepository(AbstractImageRepository):

    @classmethod
    def save_image(cls, side_of_pear: SideOfPear, binary_image: ndarray) -> None:
        if not constants.SAVE_BINARY_IMAGE_FLG:
            return None

        save_dir_name = constants.SAVE_BINARY_IMAGE_PATH + '/' + side_of_pear.get_dir_name()
        super().make_directory(dir_name=save_dir_name)

        save_file_name = save_dir_name + '/' + side_of_pear.get_file_name()
        cv2.imwrite(save_file_name, binary_image)
