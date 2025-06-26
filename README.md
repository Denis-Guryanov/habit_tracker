# Habit Tracker

Трекер привычек с интеграцией Telegram, Celery, PostgreSQL и покрытием тестами.

## Возможности
- CRUD привычек с валидацией и правами доступа
- Публичные привычки
- Регистрация и авторизация пользователей (Token и Session)
- Пагинация (5 привычек на страницу)
- Интеграция с Telegram для напоминаний
- Отложенные задачи через Celery + Redis
- Использование переменных окружения
- Документация Swagger/Redoc
- Покрытие тестами 80%+
- CORS для фронтенда

## Быстрый старт

### 1. Клонируйте репозиторий и установите Poetry
```bash
poetry install
```

### 2. Настройте переменные окружения
Создайте файл `.env` в корне проекта:
```
SECRET_KEY=your_secret_key
DEBUG=True
POSTGRES_DB=habit_db
POSTGRES_USER=habit_user
POSTGRES_PASSWORD=habit_pass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

### 3. Настройте PostgreSQL
```sql
CREATE USER habit_user WITH PASSWORD 'habit_pass';
CREATE DATABASE habit_db OWNER habit_user;
GRANT ALL PRIVILEGES ON DATABASE habit_db TO habit_user;
```

### 4. Примените миграции
```bash
poetry run python manage.py migrate
```

### 5. Запустите сервер
```bash
poetry run python manage.py runserver
```

### 6. Запустите Celery worker и beat
```bash
poetry run celery -A config worker -l info
poetry run celery -A config beat -l info
```

### 7. Документация
- Swagger: http://localhost:8000/swagger/
- Redoc: http://localhost:8000/redoc/

### 8. Тесты и flake8
```bash
poetry run pytest habits/tests.py --cov=habits
poetry run flake8 . --exclude=migrations
```

## Telegram интеграция
- Получите токен у @BotFather и укажите его в .env
- В привычке укажите chat_id пользователя Telegram (можно получить, написав /start вашему боту)

## Автор
Реализовано в рамках курсовой работы. Все вопросы — в Issues. 