# -*- coding: utf-8 -*-

import os


class AbstractImageRepository:

    def __init__(self):
        pass

    @classmethod
    def make_directory(cls, dir_name: str) -> None:
        if not cls.is_exist_directory(dir_name):
            os.makedirs(dir_name)
        return None

    @staticmethod
    def is_exist_directory(dir_name: str) -> bool:
        return os.path.exists(dir_name)
