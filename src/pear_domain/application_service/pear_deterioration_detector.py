""" -*- coding: urf-8
洋ナシのオブジェクトに対して汚損の検出分類を行う
"""

from src.pear_domain.entity.pear import Pear

from src.pear_domain.domain_service.background_remover import BackgroundRemover
from src.pear_domain.domain_service.deterioration_classifier import DeteriorationClassifier
from src.pear_domain.domain_service.labeling_processor import LabelingProcessor


class PearDeteriorationDetector:

    def __init__(self):
        self.__background_remover = BackgroundRemover()
        self.__deterioration_classifier = DeteriorationClassifier()
        self.__labeling_processor = LabelingProcessor()

    @property
    def background_remover(self):
        pass

    @property
    def deterioration_classifier(self):
        pass

    @property
    def labeling_processor(self):
        pass

    @background_remover.getter
    def background_remover(self):
        return self.__background_remover

    @deterioration_classifier.getter
    def deterioration_classifier(self):
        return self.__deterioration_classifier

    @labeling_processor.getter
    def labeling_processor(self):
        return self.__labeling_processor

    def call(self, pear: Pear) -> Pear:
        self.background_remover.call(pear)
        self.labeling_processor.call(pear)
        self.deterioration_classifier.call(pear)
        return pear
