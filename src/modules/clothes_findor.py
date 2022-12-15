import cv2
import math
import numpy as np
from sklearn.metrics.pairwise import  cosine_similarity
from src.modules.upper_crop import UpperCrop
import imutils
from fastapi import HTTPException



class ClothesCompare:
  def __init__(self, threshold=0.5):
    self.croper = UpperCrop()
    self.anchor = None
    self.threshold = threshold
    self.count = 0

  def __call__(self, target_image, list_images):
    target_image = imutils.resize(target_image, height=512)
    list_images = [imutils.resize(item, height=512) for item in list_images]
    self.set_anchor(target_image)
    max_similarities = []
    for img in list_images:
      crop_images = self.croper(img)
      if len(crop_images) == 0:
          max_similarities.append(0)
          continue
      similarity = self.check_if_match(crop_images)
      max_similarities.append(np.max(similarity) if len(similarity) != 0 else 0)
    res = [{
      "match_clothes": bool(item > self.threshold),
      "confident": float(max(item, 1-item))
    } for item in max_similarities]
    return res

  def set_anchor(self, opencv_image):
    crop_images = self.croper(opencv_image)
    if len(crop_images) < 1:
        raise HTTPException(detail="Clothes not found in target", status_code=404)
    self.anchor = crop_images[0]

  def check_if_match(self, images):
    anchor_emb = np.array([self.encode_image(self.anchor)]) 
    encoded_images = np.array([self.encode_image(image) for image in images])
    similarity = cosine_similarity(anchor_emb, encoded_images)[0]
    return  similarity

  def encode_image(self, image):
      image = cv2.resize(image, (224, 224))
      return np.concatenate([
          np.bincount(image[:, :, 0].flatten(), minlength=256),
          np.bincount(image[:, :, 1].flatten(), minlength=256),
          np.bincount(image[:, :, 2].flatten(), minlength=256),
      ])