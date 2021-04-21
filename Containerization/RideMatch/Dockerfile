FROM python:3.8-alpine

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

ADD . /app

EXPOSE 8001

CMD python3 ride_sharing_service.py