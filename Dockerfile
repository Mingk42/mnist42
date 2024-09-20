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
RUN pip install --no-cache-dir --upgrade git+https://github.com/Mingk42/mnist42.git@0.5.1

CMD ["sh", "run.sh"]
