FROM python:alpine

RUN apk add --no-cache postgresql-dev gcc musl-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV DATABASE_HOST=$DATABASE_HOST
ENV DATABASE_PORT=$DATABASE_PORT
ENV DATABASE_USER=$DATABASE_USER
ENV DATABASE_PASSWORD=$DATABASE_PASSWORD
ENV DATABASE_NAME=$DATABASE_NAME
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

COPY . ./

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8080"]