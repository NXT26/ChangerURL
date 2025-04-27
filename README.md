# ChangerURL

ChangerURL — это асинхронный API-сервис для сокращения ссылок, создания QR-кодов и сбора аналитики переходов.
Проект позволяет быстро создавать короткие URL, отслеживать статистику кликов и интегрироваться с системами мониторинга.

---

## 🚀 Функционал

- Генерация коротких ссылок для любых URL.
- Перенаправление по коротким ссылкам на оригинальный адрес.
- Получение статистики переходов по ссылке.
- Деактивация ссылок (запрет на использование).
- Генерация QR-кодов для коротких ссылок.
- Сбор метрик работы сервиса для мониторинга через Prometheus и Grafana.
- Скрипты для симуляции кликов и наполнения тестовыми данными.

---

## 🛠️ Стек технологий

- Python 3.9
- FastAPI — высокопроизводительный API
- SQLAlchemy (async) — работа с PostgreSQL
- PostgreSQL — основная база данных
- Alembic — миграции схемы базы
- Prometheus — сбор метрик
- Grafana — визуализация мониторинга
- Docker + Docker Compose — контейнеризация проекта
- pytest — тестирование

---

## 📁 Структура проекта

```
ChangerURL/
├── app/                  # Основной код приложения
│   ├── crud.py           # Операции с базой данных
│   ├── models.py         # SQLAlchemy модели
│   ├── routes.py         # Эндпоинты FastAPI
│   ├── db.py             # Подключение к базе
│   ├── main.py           # Инициализация приложения
│   ├── metrics.py        # Метрики Prometheus
│   └── schemas.py        # Pydantic схемы
│
├── alembic/              # Миграции базы данных
├── tests/                # Тесты на pytest
├── data/                 # Тестовые данные
├── simulate_clicks.py    # Скрипт генерации кликов
├── populate_test_data.py # Скрипт создания тестовых ссылок
├── docker-compose.yml    # Конфигурация docker-compose
├── Dockerfile            # Dockerfile для сборки контейнера
├── requirements.txt      # Зависимости проекта
├── prometheus.yml        # Конфигурация Prometheus
├── alembic.ini           # Конфигурация Alembic
└── .env                  # Переменные окружения
```

---

## ⚙️ Установка и запуск через Docker

### 1. Клонирование репозитория

```bash
git clone https://github.com/NXT26/ChangerURL.git
cd ChangerURL
```

### 2. Настройка окружения

Создайте файл `.env` в корне проекта на основе примера:

```bash
POSTGRES_HOST=postgres
POSTGRES_PORT=port
POSTGRES_DB=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
```

(если используете Docker Compose — используйте именно `POSTGRES_HOST=postgres`)

### 3. Запуск проекта

```bash
docker compose up --build
```

После запуска сервисы будут доступны по адресам:

| Сервис | Адрес |
|:---|:---|
| FastAPI API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3001 |

**Доступ в Grafana:**
- Логин: `admin`
- Пароль: `admin`

---

## 📋 Использование API

### Swagger UI
Документация API доступна сразу после запуска:
👉 http://localhost:8000/docs

### Основные эндпоинты

| Метод | Путь | Описание |
|:-----:|:-----|:---------|
| `POST` | `/shorten` | Создание короткой ссылки |
| `GET` | `/{short_code}` | Перенаправление по короткой ссылке |
| `GET` | `/stats/{short_code}` | Получение статистики по ссылке |
| `POST` | `/deactivate/{short_code}` | Деактивация короткой ссылки |
| `GET` | `/qr/{short_code}` | Генерация QR-кода для ссылки |

---

## 📊 Мониторинг и метрики

Метрики Prometheus доступны по адресу:
👉 http://localhost:8000/metrics

### Визуализация в Grafana

Подключите источник данных Prometheus через URL:
```
http://prometheus:9090
```

### Примеры графиков:

| Название | Запрос |
|:---|:---|
| Запросы по эндпоинтам | `sum(rate(http_requests_total[1m])) by (handler)` |
| Ошибки 4xx | `sum(rate(http_requests_total{status=~"4.."}[1m])) by (handler)` |
| Доли статусов | `sum(rate(http_requests_total[5m])) by (status)` |
| Среднее время ответа | `rate(http_server_requests_duration_seconds_sum[5m]) / rate(http_server_requests_duration_seconds_count[5m])` |
| 95-й перцентиль времени ответа | `histogram_quantile(0.95, sum(rate(http_server_requests_duration_seconds_bucket[5m])) by (le))` |

---

## 🧪 Тестирование

Запуск тестов:

```bash
pytest tests/
```

(в тестах используется отдельная база и фейковые данные)

---

## 📸 Пример дашборда Grafana

<img width="1169" alt="Снимок экрана 2025-04-27 в 13 13 30" src="https://github.com/user-attachments/assets/6bcec558-5eae-4948-bcfc-502dd3ef1ef4" />

---

## 📢 Примечание

- База данных поднимается и мигрируется автоматически при старте контейнеров.
- Все метрики автоматически собираются и доступны для мониторинга сразу после запуска.

---

## 🧠 Контакты

Разработчик: [NXT26](https://github.com/NXT26)

---

> Проект активно развивается и открыт для улучшений 🚀


