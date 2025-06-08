# Архитектура проекта

## Общая структура

- **Frontend**: статический HTML/CSS/JS интерфейс, Python-скрипты по необходимости.
- **Backend**: Python (FastAPI или Flask). Обрабатывает API-запросы, общается с базой данных.
- **Database**: PostgreSQL, инициализация и миграции — через скрипты.

## Поток данных

Пользователь → HTML-форма → JS скрипт → API → Python (обработка) → PostgreSQL

## Пример эндпоинта:

```
POST /api/analyze
Body: {{ csv_data }}
Response: {{ prediction_result }}
```
