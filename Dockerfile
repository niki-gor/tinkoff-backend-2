FROM python:alpine3.17 AS builder

WORKDIR /opt/app
COPY ./requirements.txt ./
RUN python3.11 -m venv --copies venv
RUN venv/bin/pip install -r requirements.txt
COPY ./ ./
EXPOSE 8081/tcp
ENTRYPOINT ["venv/bin/python", "-m", "forum"]
