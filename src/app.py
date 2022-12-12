from typing import List
from fastapi import FastAPI, File, UploadFile
from src import utils

from src.modules import FaceFindor
from src.modules import ClothesCompare, MyOCR, OCRResult


app = FastAPI()
face_findor = FaceFindor()
clothes_findor = ClothesCompare()
my_ocr = MyOCR()

@app.post("/face-findor")
async def create_upload_files(list_images: List[UploadFile], target_image: UploadFile=File()):
    BGR_target_image = await utils.file2opencv(target_image)
    BGR_list_images = [await utils.file2opencv(file) for file in list_images]
    index2file_name = [file.filename for file in list_images]
    results = face_findor(BGR_target_image, BGR_list_images)
    response = {index2file_name[int(key)]: results[key] for key in results}
    return response


@app.post("/clothes-findor")
async def clothes_findor_endpoint(list_images: List[UploadFile], target_image: UploadFile=File()):
    BGR_target_image = await utils.file2opencv(target_image)
    BGR_list_images = [await utils.file2opencv(file) for file in list_images]
    index2file_name = [file.filename for file in list_images]
    results = clothes_findor(BGR_target_image, BGR_list_images)
    print(results)
    response = {index2file_name[int(key)]: results[key] for key in range(len(results))}
    return response


@app.post("/ocr")
async def ocr_detect(image: UploadFile=File()):
    image_converted = await utils.file2opencv(image)
    result_list: List[OCRResult] = my_ocr.detect(image_converted)
    return result_list