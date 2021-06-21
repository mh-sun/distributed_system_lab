FROM python:3.8-alpine

RUN mkdir /rating_service
WORKDIR /rating_service

ADD requirements.txt /rating_service/requirements.txt
RUN pip install -r /rating_service/requirements.txt

ADD . /rating_service

CMD ["python","/rating_service/rating_service.py"]