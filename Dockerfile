FROM python:3.10.1-slim-bullseye

MAINTAINER gmrv

ENV PYTHONUNBUFFERED 1

RUN unlink /etc/localtime && ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime
RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
