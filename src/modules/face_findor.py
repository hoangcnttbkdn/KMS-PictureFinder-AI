import numpy as np
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

class FaceFindor:
    def __init__(self, *arg, **karg):
        self.app = FaceAnalysis(allowed_modules=['detection', 'alignment', 'recognition'])
        self.app.prepare(ctx_id=0, det_size=(640, 640))
    
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
        predict = self.app.get(target_image)
        portrait_emb = predict[0]["embedding"] # Just get first embedding with shape 1x512
        # portrait_face = self.crop_image(target_image, predict[0]["bbox"], reverse_channel=True)

        result = dict()
        idx = 0
        for image in list_images:
            keyIdx = str(idx)
            result[keyIdx] = dict()
            predict = self.app.get(image)
            contains_embs =  [item["embedding"] for item in predict] # With shape (num_face, 512)
            contains_bboxes =  [item["bbox"] for item in predict] # With shape (num_face, 512)
            # contains_faces = [self.crop_image(image, item["bbox"], reverse_channel=True) for item in predict]

            THRESHOLD = 0.5
            distances = cosine_similarity([portrait_emb], contains_embs)[0]

            best_match_index = np.argmax(distances)
            best_match_distance = distances[best_match_index]
            best_match_bbox = contains_bboxes[best_match_index]
            # best_match_face = contains_faces[best_match_index]
            result[keyIdx]["num_of_face"] = len(contains_embs)
            if best_match_distance > THRESHOLD:
                print(f">> Match face in first image with confidence {best_match_distance}")
                result[keyIdx]["match_face"] = True
                result[keyIdx]["face_location"] = list(map(int, best_match_bbox))
                result[keyIdx]["confident"] = float(best_match_distance)
            else:
                print(f">> No matching")
                result[keyIdx]["match_face"] = False
                result[keyIdx]["face_location"] = None
                result[keyIdx]["confident"] = 1 - float(best_match_distance)
            idx += 1
        return result
    
    @staticmethod
    def crop_image(image, bbox, reverse_channel=False):
        x1, y1, x2, y2 = bbox.astype(int)
        croped = image[y1:y2, x1:x2]
        if reverse_channel:
            return croped[:, :, ::-1]
        return croped