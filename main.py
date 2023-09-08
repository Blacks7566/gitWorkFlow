from fastapi import FastAPI, File, UploadFile
import os
from utils import genrate_image_vari

from core.config import settings

app = FastAPI()


@app.get("/")
def root():
    return {"msg": "root page of img api"}


@app.post("/gen")
async def image(timestamp: str, file: UploadFile = File(...)):
    # print("--->", file)
    filename = f"{timestamp}{file.filename[-4:]}"
    print(filename)
    context = await file.read()
    # print(context)

    with open(f"image/{filename}", "wb") as f:
        f.write(context)
    images = genrate_image_vari(filename, timestamp)
    return {"images_links": images}
