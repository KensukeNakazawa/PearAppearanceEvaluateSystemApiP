""" -*- coding: utf-8 -*-
"""
import os
import unittest

from dotenv import load_dotenv
import numpy as np

from src.pear_domain.value_object.coordinate import Coordinate
from src.pear_domain.value_object.deterioration import Deterioration
from src.pear_domain.entity.side_of_pear import SideOfPear


def generate_coordinate():
    return Coordinate(under=500, top=100, left=400, right=600)


def generate_deterioration():
    return Deterioration(area_rate=0.4, deterioration_class=1)


def generate_side_of_pear():
    mock_image = np.zeros((224, 224, 3)).astype('float')
    return SideOfPear(mock_image)


def unittest_call():
    load_dotenv()
    print(os.getenv('ENVIRONMENT'))
    unittest.main()

