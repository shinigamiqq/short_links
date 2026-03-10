# Short Links Service

Сервис сокращения ссылок, реализованный на **FastAPI**.
Позволяет создавать короткие ссылки, управлять ими и получать статистику использования.

---

# Возможности

## Основные функции

* Создание короткой ссылки
* Перенаправление по короткой ссылке
* Удаление ссылки
* Изменение оригинального URL
* Получение статистики переходов
* Поиск ссылки по оригинальному URL
* Кастомные alias для ссылок
* Указание времени жизни ссылки

## Дополнительно

* Простая регистрация пользователей
* Redis кэширование
* PostgreSQL база данных
* Docker / Docker Compose

---

# База данных

Используется **PostgreSQL**.

## Таблица users

| Поле          | Тип     |
| ------------- | ------- |
| id            | integer |
| email         | string  |
| password_hash | string  |

## Таблица links

| Поле         | Тип          |
| ------------ | ------------ |
| id           | integer      |
| original_url | string       |
| short_code   | string       |
| created_at   | datetime     |
| expires_at   | datetime     |
| clicks       | integer      |
| last_used    | datetime     |
| user_id      | integer (FK) |

---

# Кэширование

Используется **Redis**.

Кэшируются:

* соответствие `short_code -> original_url`

Это ускоряет перенаправление по популярным ссылкам.

Кэш очищается при:

* удалении ссылки
* изменении ссылки

---

# API

Swagger документация доступна по адресу:

```
http://localhost:8000/docs
```

---

# 1. Создание короткой ссылки

```
POST /links/shorten
```

### Request

```json
{
  "original_url": "https://google.com",
  "custom_alias": "google",
  "expires_at": "2026-12-01T12:00"
}
```

### Response

```json
{
  "short_url": "http://localhost:8000/google"
}
```

---

# 2. Переход по короткой ссылке

```
GET /{short_code}
```

Пример:

```
GET /google
```

Пользователь будет перенаправлен на оригинальный URL.

---

# 3. Получение статистики

```
GET /links/{short_code}/stats
```

### Response

```json
{
  "original_url": "https://google.com",
  "created_at": "2025-05-01T12:00:00",
  "clicks": 10,
  "last_used": "2025-05-02T10:10:00"
}
```

---

# 4. Поиск ссылки по оригинальному URL

```
GET /links/search?original_url=https://google.com
```

---

# 5. Обновление ссылки

```
PUT /links/{short_code}
```

### Request

```json
{
  "original_url": "https://openai.com"
}
```

---

# 6. Удаление ссылки

```
DELETE /links/{short_code}
```

---

# 🐳 Запуск проекта

## 1. Клонирование репозитория

```bash
git clone <repo_url>
cd url-shortener
```

## 2. Запуск через Docker

```bash
docker compose up --build
```

После запуска сервис будет доступен:

```
http://localhost:8000
```

Swagger документация:

```
http://localhost:8000/docs
```

---

# Переменные окружения

Можно задать через `.env` файл.

```
DATABASE_URL=postgresql://postgres:postgres@db:5432/shortener
REDIS_URL=redis://redis:6379
JWT_SECRET=secret
```

---

# Пример использования

1. Создать ссылку

```
POST /links/shorten
```

2. Получить короткую ссылку

```
http://localhost:8000/abc123
```

3. Перейти по ссылке

→ произойдет redirect на оригинальный URL

4. Посмотреть статистику

```
GET /links/abc123/stats
```

---

# Используемые технологии

* FastAPI
* PostgreSQL
* Redis
* SQLAlchemy
* Docker
* Uvicorn

---
