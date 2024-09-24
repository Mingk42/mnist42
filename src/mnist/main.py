from typing import Annotated
from fastapi import FastAPI, File, UploadFile

import os
from tz_kst import now
from mnist import db

app = FastAPI()


@app.get("/")
def idx():
    return {"Hello":"n11", "conn":"ok", "now":now()}

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
#    from datetime import datetime, timezone, timedelta

#     KST = timezone(timedelta(hours=9))
#     dt = datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')
    dt = now()

#     import re
#     if not re.search(re.compile("^(image/)\w*"), ):
#         return "올바르지 않은 형식, 이미지 파일을 넣어주세요"
    # 파일저장
    # 파일저장 경로 db insert
    # tablename    image_processing
    # colume : num (초기 인서트, 자동증가)
    # colume : filename, file path, req time, req user
    # coluem : pred model, pred rst, pred time

    type, file_ext = file.content_type.split("/")

    if type != "image":
        return "올바르지 않은 형식, 이미지 파일을 넣어주세요"

    img = await file.read()

    import uuid

    file_name = file.filename
    upload_dir = os.getenv("UPLOAD_PATH",f"{os.path.dirname(os.path.abspath(__file__))}/img/")
    os.makedirs(upload_dir,exist_ok=True)

    file_full_path = os.path.join(upload_dir, f"{uuid.uuid4()}.{file_ext}")

    with open(file_full_path, "wb") as f:
        f.write(img)

    ##### DB PROCESS #################################################
    db.mk_image_processing()        # DB 없으면 생성

    sql = f"INSERT INTO image_processing(file_name, file_path, request_time, request_user) VALUES ('{file.filename}', '{file_full_path}', '{dt}', 'n11')"
    row_cnt=db.dml(sql, )
    ##### DB PROCESS END #############################################

    return {
            "filename": file.filename,
            "content_type":file.content_type,
            "file_full_path":file_full_path,
            "row_cnt":row_cnt
            }

@app.get("/all")
def read_all():
    return db.select("all")


@app.get("/one")
def read_one():
    return db.select("one")

@app.get("/last_one")
def read_one():
    return db.select("last_one")

@app.get("/many")
def read_many(size:int=-1):
    return db.select("many", size)


@app.delete("/clear_table")
def clear_table():
    return db.truncate()

# @app.post("/predImg/")
# async def predImg(file: UploadFile):