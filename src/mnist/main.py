from typing import Annotated
from fastapi import FastAPI, File, UploadFile

import os
from tz_kst import now
from mnist import db

app = FastAPI()


@app.get("/")
def idx():
    """
    Index

    - Args:
        - None

    - Returns:
        - Hello: n11의 소유임을 표시
        - conn: ok, 연결 잘 됨 표시
        - now: 현재 서울 시간
    """
    return {"Hello":"n11", "conn":"ok", "now":now()}

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    """
    # 미사용
    """

    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, label:int):
    """
    예측하고자 하는 이미지 파일을 올립니다.

    - Args:
        - file: 이미지 파일, 이미지 외의 형식 업로드 불가
        - label: 예측의 정답 (int)

    - Returns:
        - filename: 파일의 원 명칭
        - content_type: 파일 형식
        - file_full_path: 파일이 저장된 위치의 전체경로
        - row_cnt: 쿼리 결과의 길이 (항상 1)
    """
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

    # label 추가
    # sql = f"INSERT INTO image_processing(file_name, file_path, request_time, request_user) VALUES ('{file.filename}', '{file_full_path}', '{dt}', 'n11')"
    #############
    sql = f"INSERT INTO image_processing(file_name, file_path, request_time, request_user, label) VALUES ('{file.filename}', '{file_full_path}', '{dt}', 'n11', '{label}')"
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
    """
    DB 안의 모든 데이터를 불러옵니다.

    - Args:
        - None

    - Returns:
        - DB 내의 모든 데이터 (list)
    """
    return db.select("all")


@app.get("/one")
def read_one():
    """
    DB 안의 데이터 1개를 불러옵니다. (첫 번째 데이터임)

    - Args:
        - None

    - Returns:
        - DB 내의 데이터 (dict)
    """
    return db.select("one")

@app.get("/last_one")
def read_one():
    """
    DB 안의 데이터 중 마지막 1개를 불러옵니다.

    - Args:
        - None

    - Returns:
        - DB 내의 마지막 데이터 (dict)
    """
    return db.select("last_one")

@app.get("/many")
def read_many(size:int=-1):
    """
    DB 안의 데이터를 n개 불러옵니다.

    - Args:
        - size: 불러올 데이터의 갯수 (int), 음수 입력 시 (전체 - 입력한 갯수)

    - Returns:
        - DB 내의 n개 데이터 (list)
    """
    return db.select("many", size)


@app.delete("/clear_table")
def clear_table():
    """
    DB를 모두 비우고, num을 1로 리셋합니다

    - Args:
        - None

    - Returns:
        - AUTO_INCREMENT: 1 (reseted serial value)
    """
    return db.truncate()

# @app.post("/predImg/")
# async def predImg(file: UploadFile):