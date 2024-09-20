import pymysql.cursors
import os


def connect(host=os.getenv("DB_IP","localhost"),user='mnist',password='1234',database='mnistdb',port=int(os.getenv("DB_PORT","53306"))):
    # Connect to the database
    conn = pymysql.connect(
        host= host,
        user= user,
        password= password,
        database= database,
        port= port,
        cursorclass= pymysql.cursors.DictCursor
    )

    return conn

def mk_image_processing():
    connection = connect()

    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = """
                -- CREATE OR REPLACE TABLE image_processing (
                CREATE TABLE IF NOT EXISTS image_processing (
                    num INT AUTO_INCREMENT PRIMARY KEY COMMENT '시리얼',
                    file_name VARCHAR(100) NOT NULL COMMENT '원본 파일명',
                    file_path VARCHAR(255) NOT NULL COMMENT '저장 전체 경로 및 변환 파일명',
                    request_time VARCHAR(50) NOT NULL COMMENT '요청시간',
                    request_user VARCHAR(50) NOT NULL COMMENT '요청 사용자',
                    prediction_model VARCHAR(100) COMMENT '예측 사용 모델',
                    prediction_result VARCHAR(50) COMMENT '예측 결과',
                    prediction_time VARCHAR(50) COMMENT '예측 시간'
            )
            """
            cursor.execute(sql)

    return None

def select(fetchMethod:str="all",fetchN:int=-1):
    connection = connect()

    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM image_processing"
            cursor.execute(sql, )
            ######  fetch 갯수 분기 #######################
            if fetchMethod=="all":
                result = cursor.fetchall()
            elif  fetchMethod=="one":
                result = cursor.fetchone()
            elif  fetchMethod=="many":
                result = cursor.fetchmany(fetchN)
            elif  fetchMethod=="last_one":
                if cursor.rowcount>1:
                    result = cursor.fetchall()[-1]
                else:
                    result = None
            else:
                raise Error("!!! Undefined Arguments")
            ######  fetch 갯수 분기 끝 #####################

    return result

def truncate():
    connection = connect()

    ##### DB CONNECT #################################################
    with connection:
        with connection.cursor() as cursor:
            sql = "TRUNCATE TABLE image_processing"
            cursor.execute(sql, )

            sql ="SELECT AUTO_INCREMENT FROM information_schema.tables WHERE table_name='image_processing'"
            cursor.execute(sql, )
            result = cursor.fetchone()
    ##### DB CONNECT END #############################################

    return result


def dml(sql:str):
    connection = connect()

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, )
        connection.commit()
        rowcnt=cursor.rowcount

    return rowcnt


def get_train_data():
    connection = connect()

    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT num FROM image_processing WHERE prediction_result IS NULL"
            cursor.execute(sql, )
            result = cursor.fetchone()

    return result["num"]