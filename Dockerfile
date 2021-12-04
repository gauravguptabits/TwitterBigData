FROM python:3.8.12
RUN apt-get update
ADD . /TwitterBigData
WORKDIR /TwitterBigData
RUN pip install -r requirements.txt
