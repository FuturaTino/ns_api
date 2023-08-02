# syntax=docker/dockerfile:1
FROM python:3.9-alpine

WORKDIR /app
COPY . .
# COPY requirements.txt /app/requirements.txt
# dependencies
RUN apk update && apk add --no-cache build-base libffi-dev openssl-dev
RUN python -m pip install --upgrade pip
RUN pip install -U pip setuptools
RUN pip install -r requirements.txt


EXPOSE 8080
CMD ["python" , "app.py"]