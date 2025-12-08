# Payouts Service

Сервис для создания и асинхронной обработки заявок на выплаты.  
Использует Django, DRF, Celery, Redis и PostgreSQL.


Можно запускать сервис двумя способами:

- Локально (Windows / Linux) с `docker-compose.services.yml` (Postgres + Redis + PgAdmin)
Django, Celery и тесты **запускаются локально**, а инфраструктура — через `docker-compose.services.yml`.
- Через docker - `docker-compose.prod.yml`

---

#  1. Запуск локально

### Python 3.11+
### Создание и запуск виртуального окружения
```
python -m venv venv
```
Windows (Git Bash): ``` . venv/Scripts/activate ```
Linux: ``` source venv/bin/activate ```

### Установка зависимостей
```
pip install -r payouts_project/requirements.txt
```

### Создание .env файла на подобии .env.example
```
# Postgres
POSTGRES_DB=payouts_db
POSTGRES_USER=payouts_user
POSTGRES_PASSWORD=payouts_pass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Django
DJANGO_SECRET_KEY=django_secret_key
DJANGO_DEBUG=True

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@local.dev
PGADMIN_DEFAULT_PASSWORD=admin123

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Запуск сервисов (PostgreSQL, Redis, PgAdmin)
```
docker compose -f docker-compose.services.yml up -d
```

Проверить, что всё работает:

Redis → `localhost:6379`
PostgreSQL → `localhost:5432`
PgAdmin → [http://localhost:15433](http://localhost:15433)

### Применение миграций и сбор статики
Перейдите в каталог **payouts_project**:
```
cd payouts_project
```
Примените миграции и собирите статику:
```
python manage.py migrate

python manage.py collectstatic --noinput
```

### Запуск тестов
```
python manage.py test -v 2
```

### Запуск Celery worker
Windows
```
celery -A payouts_project worker -l info -P solo
```
Linux
```
celery -A payouts_project worker -l info --concurrency=4
```

- Запуск Django сервера (локально)
```
python manage.py runserver
```
После запуска:
```
http://127.0.0.1:8000/api/payouts/
```
Документация Swagger / Redoc:
```
/api/docs/swagger/
/api/docs/redoc/
```

---

#  2. Запуск через Docker

### Создание .env файла на подобии .env.example
```
# Postgres
POSTGRES_DB=payouts_db
POSTGRES_USER=payouts_user
POSTGRES_PASSWORD=payouts_pass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Django
DJANGO_SECRET_KEY=django_secret_key
DJANGO_DEBUG=True

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@local.dev
PGADMIN_DEFAULT_PASSWORD=admin123

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Запуска docker compose
```
docker-compose -f docker-compose.prod.yml up
```

---

#  3. Описание деплоя


## Как можно представить деплой проекта в прод

В продакшне проект разворачивается как набор сервисов, работающих согласованно друг с другом.
Обычно это:

* API - Django backend,
* Celery для асинхронных задач,
* брокер сообщений (Redis, rabbitmq),
* база данных (PostgreSQL),
* дополнительный сервис для статических файлов и балансировки (nginx).

Приложение запускается в отдельной изолированной среде (виртуальная машина, контейнеры).
Код публикуется через систему CI/CD, которая выполняет сборку, тесты и развертывание.
Проект разворачивается на тестовом стенде, где происходят тесты (ветка test, PR и ревью feature -> test). Правки. Деплой на дев стенд, где происходит тестирование в прод формате (ветка dev, PR -> dev). И далее на прод (ветка prod/main/master, PR -> prod).

## **Какие сервисы необходимы**

Для корректной работы нужно минимум:

1. **Django-приложение** — API сервиса выплат.
2. **PostgreSQL** — хранилище заявок и статусов.
3. **Redis**/**Rabbitmq** — брокер задач Celery.
4. **Celery Worker** — выполнение фоновых задач обработки выплат.
6. **Веб-сервер** (например, nginx) — для отдачи статики и проксирования запросов к Django.

---

## **Как бы запускался Django и Celery в реальной системе**

В реальном продакшне приложение не запускают командой `runserver`.
Вместо этого используется продакшн-веб-сервер + WSGI/ASGI-процесс.

Обычно это выглядит так:

### **Django**

* Через Gunicorn или uvicorn/gunicorn-комбинацию (если ASGI).
* В составе системных сервисов или контейнеров.
* За ним стоит обратный прокси (например nginx).

Команда может выглядеть так:

```
gunicorn payouts_project.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### **Celery Worker**

Запускается как отдельный постоянный сервис:

```
celery -A payouts_project worker -l info
```

### **Docker**

Все процессы должны быть упакованы в сервисы, которые автоматически перезапускаются и логируются.

---

## **Минимальные шаги по подготовке окружения**

Ниже перечислены минимальные действия, которые необходимы для того, чтобы развернуть проект в чистой среде — без привязки к Docker, Kubernetes или конкретной инфраструктуре.

1. **Установить зависимости ОС**

   * Python 3.11+
   * PostgreSQL
   * Redis
   * pip + venv

2. **Создать виртуальное окружение**

   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. **Установить Python-зависимости**

   ```
   pip install -r requirements.txt
   ```

4. **Создать .env файл**
   (значения для БД, Redis и Django)

5. **Применить миграции**

   ```
   python manage.py migrate
   ```

6. **Собрать статику**

   ```
   python manage.py collectstatic --noinput
   ```

7. **Запустить продакшн-сервер Django**
   (Gunicorn / uvicorn)

8. **Запустить Celery worker**

   ```
   celery -A payouts_project worker -l info
   ```

9. **Настроить единый точку входа (reverse proxy)**
   Например, nginx.

10. **Настроить систему логирования и перезапуска**
    Docker.

# 4. Скрины с постмана
![alt text](<Снимок экрана 2025-12-08 111752.png>)
![alt text](<Снимок экрана 2025-12-08 111652.png>)
![alt text](<Снимок экрана 2025-12-08 111602.png>)
![alt text](<Снимок экрана 2025-12-08 111456.png>)
![alt text](<Снимок экрана 2025-12-08 110820.png>)
![alt text](<Снимок экрана 2025-12-08 110758.png>)