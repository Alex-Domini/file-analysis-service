# File Analysis Service

Тестовое задание на FastAPI.

Сервис скачивает текстовые файлы из внешнего API, сохраняет их локально, хранит информацию о них в базе данных и вычисляет статистику количества цифр (0–9) в выбранных файлах.

---

## Возможности

- Загрузка файлов из внешнего API
- Отображение статуса загрузки в реальном времени
- Возможность остановить загрузку
- Сохранение файлов на диск
- Хранение информации о скачанных файлах в SQLite
- Просмотр списка скачанных файлов
- Пагинация списка файлов
- Выбор отдельных файлов
- Выбор всех файлов
- Расчёт статистики количества цифр

---

## Используемый стек
- Python
- FastAPI
- SQLAlchemy
- SQLite
- httpx
- Jinja2
- Docker

---

## Структура проекта

```
file-analysis-service
├─ app
│  ├─ api
│  │  ├─ dependencies.py
│  │  └─ routers
│  │     ├─ download.py
│  │     ├─ files_router.py
│  │     ├─ web_router.py
│  │     └─ __init__.py
│  ├─ clients
│  │  └─ file_api_client.py
│  ├─ core
│  │  ├─ base.py
│  │  ├─ config.py
│  │  ├─ database.py
│  │  └─ paths.py
│  ├─ models
│  │  └─ file.py
│  ├─ repositories
│  │  └─ downloaded_file_repository.py
│  ├─ schemas
│  │  ├─ download_status.py
│  │  ├─ file.py
│  │  └─ file_statistics.py
│  ├─ services
│  │  ├─ download_state.py
│  │  ├─ download_task_service.py
│  │  ├─ file_service.py
│  │  ├─ file_statistics_service.py
│  │  └─ file_storage_service.py
│  ├─ static
│  │  ├─ css
│  │  │  └─ style.css
│  │  └─ js
│  │     ├─ app.js
│  │     └─ files.js
│  ├─ templates
│  |  ├─ files.html
│  |  └─ index.html
|  └─ main.py
|─ storage
├─ .dockerignore
├─ docker-compose.yml
├─ Dockerfile
├─ README.md
└─ requirements.txt

```

---

## Запуск проекта

Клонировать репозиторий

```bash
git clone https://github.com/Alex-Domini/file-analysis-service.git
```

Перейти в папку проекта

```bash
cd file-analysis-service
```

Запустить Docker

```bash
docker compose up --build
```

После запуска приложение будет доступно по адресу

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

---

## Использование

### 1. Скачать файлы

На главной странице нажать кнопку

```
Скачать файлы
```

Во время загрузки отображается

- текущий статус
- количество скачанных файлов
- текущий пакет
- ошибки (если возникли)

Также загрузку можно остановить.

---

### 2. Просмотр файлов

Перейти на страницу

```
Список файлов
```

Доступны

- список файлов
- пагинация
- выбор файлов
- выбор всех файлов

---

### 3. Расчёт статистики

Выбрать необходимые файлы и нажать

```
Произвести расчеты
```

Будет показана

- общая статистика
- статистика по каждому выбранному файлу

---

## Конфигурация

Основные настройки находятся в `.env`

Пример

```env
BASE_API_URL=http://91.199.149.128:18001
CANDIDATE_ID = "Candidate Name"
```

---

## Что реализовано

- асинхронная работа с внешним API
- повторные попытки при ошибках 403 и 429
- хранение файлов локально
- хранение информации в SQLite
- пагинация
- выбор файлов
- выбор всех файлов
- расчёт статистики
- Docker
- Swagger

---

Тестовое задание выполнено на Python с использованием FastAPI.