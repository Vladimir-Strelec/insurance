FROM python:3.12.3

WORKDIR /app

RUN apt-get update && apt-get install -y nginx

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /app/media /app/static

CMD service nginx start && gunicorn myproject.wsgi:application --bind 127.0.0.1:8000

