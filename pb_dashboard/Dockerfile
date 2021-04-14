FROM python:3.8-slim

RUN pip install poetry

ENV CONTAINER_HOME=/usr/src/app/

RUN mkdir -p ${CONTAINER_HOME}

ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME

RUN poetry install