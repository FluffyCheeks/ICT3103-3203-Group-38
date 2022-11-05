FROM python:latest

LABEL maintainer="pastelluna.tk"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./pastelLuna/pastelLuna /app

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN ls
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

