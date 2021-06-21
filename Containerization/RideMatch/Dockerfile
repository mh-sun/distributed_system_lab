FROM python:3.8-alpine

RUN mkdir /ride_service
WORKDIR /ride_service

ADD requirements.txt /ride_service/requirements.txt
RUN pip install -r /ride_service/requirements.txt

ADD . /ride_service

CMD ["python","/ride_service/ride_sharing_service.py"]