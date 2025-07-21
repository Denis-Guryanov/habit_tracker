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

---

## 🚀 Запуск через Docker Compose

1. Скопируйте пример .env и настройте переменные:

```env
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*
POSTGRES_DB=habit_db
POSTGRES_USER=habit_user
POSTGRES_PASSWORD=habit_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

2. Запустите все сервисы одной командой:
```bash
docker-compose up --build
```

3. Проект будет доступен на http://localhost (Nginx), Django — на 8000, статика/медиа — через Nginx.

---

## ⚙️ CI/CD и автодеплой

- Все коммиты в ветку `master` автоматически:
  - проходят тесты и линтинг (на SQLite)
  - проверяют сборку Docker-образов
  - деплоятся на сервер через SSH (GitHub Actions)

### Как настроить деплой:
1. На сервере установить Docker и Docker Compose.
2. Клонировать репозиторий в нужную папку.
3. Добавить SSH-ключ деплоя в GitHub Secrets:
   - `SERVER_HOST` — IP или домен сервера
   - `SERVER_USER` — пользователь для SSH
   - `SERVER_SSH_KEY` — приватный ключ (без пароля)
   - `SERVER_PORT` — порт SSH (обычно 22)
4. В workflow путь `/path/to/your/project` заменить на путь к проекту на сервере.

---

## 🧪 Тесты и локальная разработка
- Для CI тесты идут на SQLite (быстро, не требует БД).
- Для локальной разработки можно использовать Poetry или Docker Compose.

---

## 📄 Пример .env для Docker Compose
```env
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*
POSTGRES_DB=habit_db
POSTGRES_USER=habit_user
POSTGRES_PASSWORD=habit_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

---

## 🖥️ Сервер
- Убедитесь, что сервер готов к работе с Docker и Docker Compose.
- Откройте SSH-доступ для деплоя через GitHub Actions.
- После деплоя: `docker-compose up -d` для запуска/обновления.

--- 