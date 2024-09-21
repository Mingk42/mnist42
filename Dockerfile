FROM python:3.11

WORKDIR /app

COPY src/mnist/main.py /app/
COPY run.sh /app/run.sh

RUN apt update
RUN apt install -y cron
COPY ml-work-cronjob /etc/cron.d/ml-work-cronjob
RUN crontab /etc/cron.d/ml-work-cronjob
RUN apt install -y vim

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade git+https://github.com/Mingk42/mnist42.git@v0.4.0/worker

RUN echo DB_IP=172.17.0.1 >> /etc/environment
RUN echo LINE_TOKEN="rPekL6ew1Dhn9DmR5LTxStLllTziY48ILZOjHqsEc10" >> /etc/environment

CMD ["sh", "run.sh"]
