from paddleocr import PaddleOCR,draw_ocr
import numpy as np
from typing import List

class OCRResult:
    def __init__(self, boxes = None, text: str = None, confident: float = 0) -> None:
        self.boxes = boxes
        self.text = text
        self.confident = confident

class MyOCR:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
        print("Initialized MyOCR")
    
    def detect(self, image: np.ndarray) -> List[OCRResult]:
        detects = self.ocr.ocr(image, cls=True)
        result: List[OCRResult] = []

        for idx in range(len(detects)):
            res = detects[idx]
            for line in res:
                result.append(OCRResult(line[0], line[1][0], line[1][1]))

        return result