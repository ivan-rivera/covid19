FROM python:3.8.2-slim

RUN mkdir app/
WORKDIR /app

ENV POETRY_VERSION=1.0.5

RUN apt-get update && apt-get install make
RUN pip3 install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry check
RUN poetry install --no-interaction --no-ansi

COPY . /app

RUN make test

