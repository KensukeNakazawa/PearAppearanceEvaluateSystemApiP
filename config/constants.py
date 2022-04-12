

import os
import sys

par_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(par_dir)

# プロジェクトのルートパスの設定
PROJECT_ROOT_PATH = par_dir

# 画像の拡張子
IMAGE_EXTENSION = 'bmp'

IMAGE_DIRECTORIES = [1, 2, 3, 4, 5]

"""
Deterioration Detect
"""
# ブロック処理の際の1小ブロックのピクセル長
BLOCK_SIZE = 32
# ヒストグラムの階調数
HIST_SIZE = 32
# ラベリング処理を行う時の近傍の設定，4 or 8
LABELING_CONNECTIVITY = 8

DISTANCES = [5, 7, 9]
ANGLES = [0, 90, 180, 270]
FEATURE_NAMES = ['contrast', 'dissimilarity', 'homogeneity', 'ASM', 'correlation']

DETECTION_MODEL_GLCM_PATH: str = PROJECT_ROOT_PATH + '/src/classification_models/random_forest_h_glcm.sav'
DETECTION_MODEL_HIST_PATH: str = PROJECT_ROOT_PATH + '/src/classification_models/random_forest_rgb_hist.sav'

# for deterioration classification
CNN_INPUT_SIZE: int = 224
CNN_MODEL_PATH: str = PROJECT_ROOT_PATH + '/src/classification_models/deterioration_classification_model.hdf5'

DETERIORATION_CLASSES = [0, 1, 2, 3, 4]
DETERIORATION_CLASS_DICTIONARY: dict = {
    0: 'AN',
    1: 'IJ',
    2: 'SK',
    3: 'PN',
    4: 'CM'
}

DETERIORATION_CLASS_CODE = {
    'AN': 'alternalia',
    'IJ': 'injury',
    'SK': 'speckle',
    'PN': 'plane',
    'CM': 'chemical'
}

# BBoxに使う色(BGR)
DETERIORATION_CLASS_COLOR = {
    0: (255, 255, 0),  # cyan
    1: (214, 112, 218),  # orchid
    2: (133, 21, 199),  # mediumvioletred
    3: (0, 0, 255),  # red
    4: (71, 99, 255)  # tomato
}

# ORIGINAL_IMAGE_PATH = PROJECT_ROOT_PATH +
SAVE_IMAGE_PATH = PROJECT_ROOT_PATH + '/images/result_image'
SAVE_BLOCK_IMAGE_PATH = PROJECT_ROOT_PATH + '/images/block_image'
SAVE_BINARY_IMAGE_PATH = PROJECT_ROOT_PATH + '/images//binary_images'

SAVE_BLOCK_IMAGE_FLG = False
SAVE_BINARY_IMAGE_FLG = False
