import time
import requests
from prometheus_client import start_http_server, Gauge

CONFIDENCE_GAUGE = Gauge('prediction_confidence_score', 'Latest prediction confidence from ML API')

APP_URL = "http://localhost:32500/api/latest-confidence"

def fetch_confidence():
    try:
        response = requests.get(APP_URL, timeout=3)
        data = response.json()
        return data.get("confidence", 1.0)
    except Exception:
        return 1.0

if __name__ == "__main__":
    start_http_server(8000)
    print("Exporter running on port 8000...")
    while True:
        confidence = fetch_confidence()
        CONFIDENCE_GAUGE.set(confidence)
        time.sleep(5)