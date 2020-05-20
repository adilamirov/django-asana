FROM python:3.7-alpine

RUN apk update && apk add postgresql-dev postgresql-client gcc python3-dev musl-dev

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["./entrypoint.sh"]
