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
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        print("Initialized MyOCR")
    
    def detect(self, image: np.ndarray) -> List[OCRResult]:
        detects = self.ocr.ocr(image, cls=True)
        result: List[OCRResult] = []

        for idx in range(len(detects)):
            res = detects[idx]
            for line in res:
                result.append(OCRResult(line[0], line[1][0], line[1][1]))

        return result
    
    def detect_with_bib_code(self, images: List[np.ndarray], bib_code: str):
        match_bib = []
        for image in images:
            detects = self.ocr.ocr(image, cls=True)
            bib_code_str = ""
            is_matching = False
            for res in detects:
                if (is_matching):
                    break
                for line in res:
                    text = line[1][0]
                    bib_code_str += "|" + text
                    if bib_code == text:
                        is_matching = True
                        break
            match_bib.append({"match_bib": is_matching, "text": bib_code_str})
        return match_bib
                