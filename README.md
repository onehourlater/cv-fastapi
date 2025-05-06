## О чем репозиторий:
Изучаю FastApi и SQLAlchemy, делая WEB app, с помощью которого можно создавать и делиться своими CV.

## Зависимости:
- Нужен python3.9+
- Нужна локально развернутая postgresql база данных или установленный Docker

## Запустить локально:

Создайте и запустите виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate
```

Потом установите зависимости:

```bash
pip install -r requirements.txt
```

Создайте локальный .env файл, пример:

```bash
MEDIA_FOLDER_PATH=/usr/local/opt/cv-fastapi/media

POSTGRES_HOSTNAME=localhost
POSTGRES_DB=dbname
POSTGRES_USER=dbuser
POSTGRES_PASSWORD=dbpassword
POSTGRES_PORT=5432

JWT_SECRET=somesecret
JWT_ALGORITHM=HS256
# 5 mins
JWT_EXPIRES=300
# 30 days
JWT_REFRESH_EXPIRES=2592000
```

**Примечание:**
media папка по пути MEDIA_FOLDER_PATH создастся автоматически (код создания в app/main.py)

Запустите DEV сервер:

```bash
poe uvicorn
```

Сервер запустится по адресу: [http://localhost:8000](http://localhost:8000)

API docs можно посмотреть тут: [http://localhost:8000/docs](http://localhost:8000/docs)

## Запустить через Docker:

```bash
# для запуска только postgres контейнера
docker compose up postgres

# для запуска postgres и fastapi контейнеров
docker compose up
```
