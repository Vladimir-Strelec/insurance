# Используем Python
FROM python:3.12.3

# Создаем рабочую папку
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Команда запуска (для gunicorn)
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
