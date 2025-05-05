## О чем репозиторий:
Изучаю FastApi и SQLAlchemy, делая WEB app, с помощью которого можно создавать и делиться своими CV.

## Зависимости:
- Нужен python3.9+
- Нужна локально развернутая postgresql база данных

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

DB_HOSTNAME=localhost
DB_NAME=dbname
DB_USER=dbuser
DB_PASSWORD=dbpassword
DB_PORT=5432

JWT_SECRET=somesecret
JWT_ALGORITHM=HS256
# 5 mins
JWT_EXPIRES=300
# 30 days
JWT_REFRESH_EXPIRES=2592000
```

Запустите DEV сервер:

```bash
poe uvicorn
```

Сервер запустится по адресу: [http://localhost:8000](http://localhost:8000)

API docs можно посмотреть тут: [http://localhost:8000/docs](http://localhost:8000/docs)
