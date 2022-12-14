from paddleocr import PaddleOCR
from src.modules.upper_crop import UpperCrop
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
        self.croper = UpperCrop()
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
        bib_code = bib_code.lower().strip()
        for image in images:
            roi_images = self.croper(image)
            detects = []
            for roi_image in roi_images:
                detects.extend(self.ocr.ocr(roi_image[:, :, ::-1], cls=True))
            confident = 1
            is_matching = False
            for res in detects:
                # if (is_matching):
                #     break
                for line in res:
                    text = line[1][0].lower().strip()
                    print(text)
                    conf = line[1][1]
                    if bib_code == text:
                        is_matching = True
                        confident = conf
                        # break
            match_bib.append({"match_bib": is_matching, "confident": confident})
        return match_bib
                