FROM python:3.9

WORKDIR /cv-fastapi
COPY . /cv-fastapi

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["poe", "uvicorn"]
