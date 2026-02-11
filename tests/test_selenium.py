import pytest
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class TestCalculator:

    @pytest.fixture(scope="class")
    def driver(self):
        chrome_options = Options()

        if os.getenv("CI"):
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")

        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def load_page(self, driver):
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

    def test_page_loads(self, driver):
        self.load_page(driver)

        assert driver.find_element(By.ID, "num1").is_displayed()
        assert driver.find_element(By.ID, "num2").is_displayed()
        assert driver.find_element(By.ID, "operation").is_displayed()
        assert driver.find_element(By.ID, "calculate").is_displayed()

    def test_addition(self, driver):
        self.load_page(driver)

        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").send_keys("5")

        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("add")

        driver.find_element(By.ID, "calculate").click()

        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )

        assert "15" in result.text

    def test_division_by_zero(self, driver):
        self.load_page(driver)

        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("10")

        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("0")

        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("divide")

        driver.find_element(By.ID, "calculate").click()

        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )

        assert "Erreur" in result.text

    def test_all_operations(self, driver):
        self.load_page(driver)

        operations = [
            ("add", "8", "2", "10"),
            ("subtract", "8", "2", "6"),
            ("multiply", "8", "2", "16"),
            ("divide", "8", "2", "4"),
        ]

        for op, num1, num2, expected in operations:
            driver.find_element(By.ID, "num1").clear()
            driver.find_element(By.ID, "num2").clear()

            driver.find_element(By.ID, "num1").send_keys(num1)
            driver.find_element(By.ID, "num2").send_keys(num2)

            select = Select(driver.find_element(By.ID, "operation"))
            select.select_by_value(op)

            driver.find_element(By.ID, "calculate").click()

            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "result"))
            )

            assert expected in result.text
            time.sleep(1)

    def test_page_load_time(self, driver):
        start_time = time.time()

        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "calculator"))
        )

        load_time = time.time() - start_time
        assert load_time < 3.0
