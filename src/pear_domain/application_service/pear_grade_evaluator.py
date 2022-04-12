""" -*- coding: utf-8 -*-
汚損分類まで終了している，洋ナシに対してgradeの評価を行う
"""
import logging
from typing import Dict

from config.constants import DETERIORATION_CLASS_DICTIONARY
from src.pear_domain.entity.pear import Pear


class PearGradeEvaluator:

    def __init__(self):
        pass

    def call(self, pear: Pear) -> Pear:
        self.__pear_grade_evaluation(pear)
        return pear

    def __pear_grade_evaluation(self, pear: Pear):

        deterioration_class_scales = {
            'AN': 0,
            'IJ': 0,
            'SK': 0,
            'PN': 0,
            'CM': 0
        }
        for side_of_pear in pear.side_of_pears:
            for deterioration in side_of_pear.deteriorations:
                if deterioration.deterioration_code == "AN":
                    deterioration_class_scales[deterioration.deterioration_code] += 1
                else:
                    deterioration_class_scales[deterioration.deterioration_code] += deterioration.area_rate

        pear.rank_id = self.__evaluate(deterioration_class_scales)

    def __evaluate(self, deterioration_class_scales: Dict[str, int]):
        grade_scales = {
            'AN': 0,
            'IJ-SK': 0,
            'PN-CM': 0
        }

        grade_scales['AN'] = deterioration_class_scales['AN']
        grade_scales['IJ-SK'] = deterioration_class_scales['IJ'] + deterioration_class_scales['SK']
        grade_scales['PN-CM'] = deterioration_class_scales['PN'] + deterioration_class_scales['CM']

        pear_rank_id = 5
        for deterioration_name, value in grade_scales.items():
            if value == 0:
                continue
            if deterioration_name == 'AN':
                grade_an = self.__grade_an(value)
                if grade_an < pear_rank_id:
                    pear_rank_id = grade_an
            if deterioration_name == 'IJ-SK':
                grade_ij_sk = self.__grade_ij_sk(value)
                if grade_ij_sk < pear_rank_id:
                    pear_rank_id = grade_ij_sk
            if deterioration_name == "PN-CM":
                grade_pn_cm = self.__grade_pn_cm(value)
                if grade_pn_cm < pear_rank_id:
                    pear_rank_id = grade_pn_cm
        return pear_rank_id
        
    @staticmethod
    def __grade_an(an_num: int) -> int:
        grade = 0
        if an_num == 1:
            grade = 5
        elif an_num <= 3:
            grade = 4
        elif an_num <= 5:
            grade = 3
        elif an_num > 5:
            grade = 2
        else: 
            grade = 1
        return grade
    
    @staticmethod
    def __grade_ij_sk(ij_sk_ratio: float) -> int:
        grade = 0
        if ij_sk_ratio <= 0.1:
            grade = 5
        elif ij_sk_ratio <= 0.3:
            grade = 4
        elif ij_sk_ratio <= 0.5:
            grade = 3
        elif ij_sk_ratio > 0.5:
            grade = 2
        else:
            grade = 1
        return grade
    
    @staticmethod
    def __grade_pn_cm(pn_cm_ratio: float) -> int:
        grade = 0
        if pn_cm_ratio <= 0.1:
            grade = 5
        elif pn_cm_ratio <= 0.3:
            grade = 4
        elif pn_cm_ratio <= 0.5:
            grade = 3
        elif pn_cm_ratio > 0.5:
            grade = 2
        else:
            grade = 1
        return grade
        
        
