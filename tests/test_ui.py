from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_frontend_sentiment():
    options = Options()
    options.binary_location = "/usr/bin/chromium" 
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("http://localhost:5000")
        time.sleep(2)

        text_input = driver.find_element(By.ID, "text-input")
        text_input.send_keys("This product is absolutely amazing!")

        submit_btn = driver.find_element(By.ID, "submit-btn")
        submit_btn.click()
        time.sleep(3)

        result = driver.find_element(By.ID, "result-output")
        assert result.text != ""
        assert any(word in result.text for word in ["POSITIVE", "NEGATIVE", "Confidence"])

    finally:
        driver.quit()
