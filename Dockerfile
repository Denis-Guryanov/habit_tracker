# syntax=docker/dockerfile:1
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Установка зависимостей системы
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Копируем pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock ./

# Установка python-зависимостей через poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Копируем проект
COPY . .

# Собираем статику (можно закомментировать, если не нужно)
RUN python manage.py collectstatic --noinput || true

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"] 