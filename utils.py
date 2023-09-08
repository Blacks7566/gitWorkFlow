from PIL import Image
from core.config import settings
import os
from botocore.exceptions import ClientError

import boto3


Session = boto3.Session(
    aws_access_key_id=settings.AWS_CLIENT_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGIN,
)


def genrate_image_vari(filename, timestamp):
    img = Image.open(f"image/{filename}")
    gray = img.convert("L")
    mid = img.resize((500, 500))
    thum = img.resize((200, 300))
    larg = img.resize((1028, 786))
    gray.save(f"image/{timestamp}_grayscale.jpg")
    mid.save(f"image/{timestamp}_mid.jpg")
    thum.save(f"image/{timestamp}_thum.jpg")
    larg.save(f"image/{timestamp}_large.jpg")
    return load_file_in_s3()


def load_file_in_s3():
    s3 = Session.client("s3")
    files = os.listdir("./image")
    img_links = []
    for file in files:
        try:
            with open(f"./image/{file}", "rb") as data:
                s3.upload_fileobj(data, settings.AWS_BUCKET, f"image-api/{file}")
            img_links.append(f"https://datablacksoul.s3.amazonaws.com/image-api/{file}")
        except ClientError as e:
            print(e)

    delete_files(files)

    return img_links


def delete_files(files):
    for file in files:
        try:
            file_path = os.path.join("./image", file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print("All files deleted successfully.")
        except OSError:
            print("Error occurred while deleting files.")
