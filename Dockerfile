FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# ✅ install CPU-only torch (FAST)
RUN pip install --no-cache-dir torch==2.3.0+cpu --index-url https://download.pytorch.org/whl/cpu

# ✅ install remaining packages (without reinstalling torch)
RUN pip install --no-cache-dir -r requirements.txt --no-deps

COPY . .
RUN mkdir -p /app/logs

EXPOSE 5000
CMD ["python", "app.py"]
