FROM python:3.8-alpine

RUN mkdir /communication_service
WORKDIR /communication_service

ADD requirements.txt /communication_service/requirements.txt
RUN pip install -r /communication_service/requirements.txt

ADD . /communication_service

EXPOSE 8080

CMD ["python","/communication_service/communication_service.py"]