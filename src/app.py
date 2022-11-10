from typing import List
from fastapi import FastAPI, File, UploadFile
from src import utils

from src.modules import FaceFindor

app = FastAPI()
face_findor = FaceFindor()

@app.post("/face-findor")
async def create_upload_files(list_images: List[UploadFile], target_image: UploadFile=File()):
    BGR_target_image = await utils.file2opencv(target_image)
    BGR_list_images = [await utils.file2opencv(file) for file in list_images]
    index2file_name = [file.filename for file in list_images]
    results = face_findor(BGR_target_image, BGR_list_images)
    response = {index2file_name[int(key)]: results[key] for key in results}
    print("aaaaa")
    print(response)
    return response
