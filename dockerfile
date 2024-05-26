FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir flask psycopg2-binary flasgger
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]