# Habit Tracker — Трекер полезных привычек

Бэкенд-сервис для формирования и отслеживания полезных привычек на основе книги «Атомные привычки» Джеймса Клира.

## Технологии

- **Django** + **DRF** — бэкенд
- **JWT** — аутентификация
- **Celery** + **Redis** — фоновые задачи
- **PostgreSQL** / **SQLite** — база данных
- **Telegram API** — уведомления
- **drf-yasg** — документация (Swagger/ReDoc)
- **Coverage** — тестирование (89% покрытие)

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

## Установка

1. Клонировать репозиторий
```
git clone https://github.com/Sofya-Ageeva/HabitTracker.git
cd HabitTracker
```

2. Создать и активировать виртуальное окружение
```
python3 -m venv venv
```
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

3. Установить зависимости
```
pip install -r requirements.txt
```

4. Создать .env (скопировать из .env.template)
```
cp .env.template .env
```
# Заполнить SECRET_KEY, настройки БД, Redis, Telegram токен

5. Применить миграции
```
python manage.py migrate
```

6. Создать суперпользователя
```
python manage.py createsuperuser
```
7. Запустить сервер
```
python manage.py runserver
```

## Тестирование существующих функций
1. Реализованы тесты c покрытием кода более чем на 80 %. 
Для запуска теста необходимо ввести в командной строке следующую команду:
```
python manage.py test
coverage run manage.py test
coverage report
```
4. Для формирования веб-отчета:
```
coverage html
```
5. Результаты тестирования содержаться в папке `htmlcov/`)
После выполнения откройте htmlcov/index.html в браузере.

