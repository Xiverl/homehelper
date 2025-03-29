# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /backend

# Копируем файлы зависимостей
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt


# Запускаем приложение
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
