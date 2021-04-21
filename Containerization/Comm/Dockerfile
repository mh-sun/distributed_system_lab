FROM python:3.8-alpine

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD . /app

EXPOSE 8003

CMD gunicorn --bind 127.0.0.1:8003 -k eventlet -w 1 --reload communication_service:app
