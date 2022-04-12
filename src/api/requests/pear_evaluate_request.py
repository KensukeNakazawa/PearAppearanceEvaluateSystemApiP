import cv2
from flask import request
import numpy as np


class PearEvaluateRequest:
    def __init__(self):
        pear_images = request.files.getlist('pear_images')
        self.images = []
        for pear_image in pear_images:
            file = pear_image.stream
            image_array = np.asarray(bytearray(file.read()), dtype=np.uint8)
            image = cv2.imdecode(image_array, 1)
            self.images.append(image)
