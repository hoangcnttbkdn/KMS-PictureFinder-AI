import numpy as np
from typing import List

class FaceFindor:
    def __init__(self, *arg, **karg):
        pass
    
    def __call__(self, target_image: np.ndarray, list_images: List[np.ndarray]):
        """
        target: BGR image contain only 1 face
        list_images: Images contain multiple face
        return:
            {
                0: {
                    num_of_face: 3,
                    match_face: True,
                    face_location: [(x1, y1), (x2, y2)],
                    confident: 0.69   
                },
                1: {
                    num_of_face: 2,
                    match_face: False,
                    face_location: [(x1, y1), (x2, y2)],
                    confident: 0.69   
                }
            }
        With 0, 1, ... is index of image in list_images
        """
        # TODO: vyhv
        print(">> Target image", target_image.shape)
        for image in list_images:
            print(">> Image with shape", image.shape)
        return {index: {
                    "num_of_face": 3,
                    "match_face": True,
                    "face_location": [(0, 0), (69, 69)],
                    "confident": 0.69   
                } for index in range(len(list_images))}