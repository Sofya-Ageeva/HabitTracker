# Habit Tracker — Трекер полезных привычек

Бэкенд-сервис для формирования и отслеживания полезных привычек на основе книги «Атомные привычки» Джеймса Клира.

## Технологии

- **Django** + **DRF** — бэкенд
- **JWT** — аутентификация
- **Celery** + **Redis** — фоновые задачи
- **PostgreSQL** / **SQLite** — база данных
- **Telegram API** — уведомления
- **drf-yasg** — документация (Swagger/ReDoc)
- **Docker** + **Docker Compose**
- **Githab Actions (CI/CD)

## Основной функционал

- Регистрация и JWT-авторизация
- CRUD привычек
- Полезные и приятные привычки
- Связь привычек (полезная → приятная)
- Валидация: время ≤ 120 сек, периодичность 1-7 дней
- Пагинация (5 привычек на страницу)
- Telegram-уведомления
- Фоновые задачи (Celery)
- Публичные привычки

## Запуск через Docker

1. Клонировать репозиторий
```
git clone https://github.com/Sofya-Ageeva/HabitTracker.git
cd HabitTracker
```

2. Создать .env и заполнить его своими данными на основе шаблона
```
cp .env.template .env
```

# Заполнить SECRET_KEY, настройки БД, Redis, Telegram токен

3. Запуск проекта
```
docker compose up -d --build
```

4. Применить миграции
```
docker compose exec web python manage.py migrate
```

5. Создать суперпользователя
```
docker compose exec web python manage.py createsuperuser
```
## Документация
- Swagger: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/



