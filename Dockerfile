FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /chatapi

WORKDIR /chatapi

COPY . /chatapi/

RUN pip3 install --upgrade pip3 && pip3 install pip-tools && pip3 install -r requirements.txt 