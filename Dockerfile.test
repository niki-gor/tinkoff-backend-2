FROM python:alpine3.17 AS builder

WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./
EXPOSE 8081/tcp
