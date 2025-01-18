# mnist

## Pull Request URL : https://github.com/Mingk42/mnist42/pull/1
#### Require
- [x] WORKER 는 주기적으로 image_processing 테이블을 읽어서 가장 오래된 요청 하나씩을 처리한다.
- [x] DNN 모델이 없는 상황에서는 일단 0~9 중에서 임의의 값을 image_processing 테이블에 업데이트 한다.
- [x] WORKER 는 pip install 하면 ml-worker 라는 cmd 로 동작하도록 하고 도커 안에서 crontab 설정으로 3분 마다 동작한다

#### Result
<img src="https://github.com/user-attachments/assets/d0762e32-f057-4165-8f11-5468f4b05620" width=75% />
<img src="https://github.com/user-attachments/assets/c00c14ca-335d-4840-9666-3dca1b18e000" width=50% />

> 3분마다 예측 완료


<details>
<summary>Fixed Error</summary>

- Docker 내부에서 아래 오류가 반복 발생
- `-e` 옵션으로 DB_IP와 LINE_TOKEN을 전달
```python
$ tail -f /var/log/worker.log
    connection = connect()
                 ^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/mnist/db.py", line 7, in connect
    conn = pymysql.connect(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 361, in __init__
    self.connect()
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 716, in connect
    raise exc
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on 'localhost' ([Errno 111] Connection refused)")

Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 649, in connect
    sock = socket.create_connection(
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/socket.py", line 863, in create_connection
    raise exceptions[0]
  File "/usr/local/lib/python3.11/socket.py", line 848, in create_connection
    sock.connect(sa)
ConnectionRefusedError: [Errno 111] Connection refused

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/bin/ml-worker", line 8, in <module>
    sys.exit(run())
             ^^^^^
  File "/usr/local/lib/python3.11/site-packages/mnist/worker.py", line 11, in run
    data=db.get_train_data()
         ^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/mnist/db.py", line 96, in get_train_data
    connection = connect()
                 ^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/mnist/db.py", line 7, in connect
    conn = pymysql.connect(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 361, in __init__
    self.connect()
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 716, in connect
    raise exc
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on 'localhost' ([Errno 111] Connection refused)")
```
- 확인사항
  - Docker 내부에서 echo $DB_IP > 정상동작
  - Docker 내부에서 python 실행 후 os.getenv > 정상동작 
  - Docker 내부에서 worker.py 모듈 강제 실행 > 정상동작
  - cronjob으로 실행하는 경우 해당 환경변수를 가져오지 못하는 현상

```python
>>> def run():
>>>     print(f"LINE_TOKEN ::: {os.getenv('LINE_TOKEN')}")
>>>     print(f"DB_IP ::: {os.getenv('DB_IP')}",end="\n\n")
>>>     .....
LINE_TOKEN ::: None
DB_IP ::: None
```

- [참고한 글](https://this-programmer.tistory.com/488)
> cron이 환경변수를 잘 못 읽는 경우가 있음
> Docker build시에 `/etc/environment`에 환경변수를 추가하도록 하면 정상동작한다고 함

- 조치사항
> `RUN echo DB_IP=172.17.0.1 >> /etc/environment`을 Dockerfile에 추가 > 정상동작 확인, 그러나 LINE_TOKEN을 같은 방식으로 처리하면 key값이 노출되므로 심각한 보안 문제
> run.sh로 해당 문제 해결, [run.sh Link](https://github.com/Mingk42/mnist42/blob/17815de9118f1ddaf92194cd5add8e090638ce85/run.sh#L5)
</details>
