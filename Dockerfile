FROM python:3

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR usr/src
COPY ./src .
ENV APP_SETTINGS="config.Config"
ENV DATABASE_URL="postgresql://postgres:postgres_1@postgres/flask_db"

# CMD ["python","manage.py", "runserver","-h","0.0.0.0","-p","5000"]

