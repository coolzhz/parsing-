

FROM python:3.9-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y wget unzip libnss3 libgconf-2-4 libxi6 libgdk-pixbuf2.0-0 libxcomposite1 libasound2 libxrandr2 libatk1.0-0 libgtk-3-0

# Установка ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    chmod +x chromedriver && \
    mv chromedriver /usr/local/bin/

# Копирование файлов проекта
COPY . /app
WORKDIR /app

# Установка Python-зависимостей
RUN pip install -r requirements.txt

# Запуск приложения
CMD ["python", "server.py"]
