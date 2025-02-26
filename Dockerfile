FROM python:3.12.1-slim

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY /pyproject.toml /poetry.lock* /app/

RUN poetry install --no-interaction --no-ansi

COPY . /app/
