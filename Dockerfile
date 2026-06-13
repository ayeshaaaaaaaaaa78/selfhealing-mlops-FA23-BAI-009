FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir torch==2.3.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt --no-deps || \
    pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/logs
EXPOSE 5000
CMD ["python", "app.py"]
