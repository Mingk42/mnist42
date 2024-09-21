import random
import os
import requests

from tz_kst import now
from mnist import db

def run():
    """image_processing 테이블을 읽어서 가장 오래된 요청 하나씩을 처리"""
    print(f"LINE_TOKEN ::: {os.getenv('LINE_TOKEN')}")
    print(f"DB_IP ::: {os.getenv('DB_IP')}",end="\n\n")

    # STEP 1
    # image_processing 테이블의 prediction_result IS NULL 인 ROW 1 개 조회 - num 갖여오기
    data= db.get_train_data()

    if data==None:
        return None

    # STEP 2
    # RANDOM 으로 0 ~ 9 중 하나 값을 prediction_result 컬럼에 업데이트
    # 동시에 prediction_model, prediction_time 도 업데이트
    pred = random.randint(0,9)
    prediction_model="randint"
    prediction_time=now()

    sql = f"""
    UPDATE image_processing
    SET prediction_model='{prediction_model}', prediction_result='{pred}', prediction_time='{prediction_time}'
    WHERE num={data}
    """
    row_cnt= db.dml(sql, )


    # STEP 3
    # LINE 으로 처리 결과 전송

    headers = {
        'Authorization': 'Bearer ' + os.getenv('LINE_TOKEN', ''),
    }

    files = {
        'message': (None, f"{data}번째 이미지의 예측결과는 {pred}입니다."),
    }

    response = requests.post('https://notify-api.line.me/api/notify', headers=headers, files=files)

    print(f"[{prediction_time}] {data}번째 이미지의 예측결과는 {pred}입니다.")

    return {
        "prediction_time":prediction_time,
        "train_data_nth":data,
        "pred":pred
    }