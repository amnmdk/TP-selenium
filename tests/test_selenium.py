import pytest
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from calculator_page import CalculatorPage


class TestCalculator:

    @pytest.fixture(scope="class")
    def driver(self):
        chrome_options = Options()

        if os.getenv("CI"):
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    @pytest.fixture
    def page(self, driver):
        calc = CalculatorPage(driver)
        calc.load_page()
        return calc

    # --- Tests de base ---

    def test_page_loads(self, driver):
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        assert "Calculatrice Simple" in driver.title
        assert driver.find_element(By.ID, "num1").is_displayed()
        assert driver.find_element(By.ID, "num2").is_displayed()
        assert driver.find_element(By.ID, "operation").is_displayed()
        assert driver.find_element(By.ID, "calculate").is_displayed()

    def test_addition(self, page):
        result = page.calculate(10, "add", 5)
        assert "Résultat: 15" in result

    def test_division_by_zero(self, page):
        result = page.calculate(10, "divide", 0)
        assert "Erreur: Division par zéro" in result

    def test_all_operations(self, page):
        operations = [
            ("add", 8, 2, "10"),
            ("subtract", 8, 2, "6"),
            ("multiply", 8, 2, "16"),
            ("divide", 8, 2, "4"),
        ]

        for op, num1, num2, expected in operations:
            result = page.calculate(num1, op, num2)
            assert f"Résultat: {expected}" in result
            time.sleep(0.5)

    # --- Test de performance (Partie 4) ---

    def test_page_load_time(self, driver):
        start_time = time.time()

        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "calculator"))
        )

        load_time = time.time() - start_time
        print(f"Temps de chargement: {load_time:.2f} secondes")

        assert load_time < 3.0, f"Page trop lente: {load_time:.2f}s"

    # --- Tests avec nombres decimaux (Partie 5.1) ---

    def test_addition_decimals(self, page):
        result = page.calculate(3.5, "add", 2.3)
        assert "Résultat: 5.8" in result

    def test_subtraction_decimals(self, page):
        result = page.calculate(10.7, "subtract", 3.2)
        assert "Résultat: 7.5" in result

    def test_multiply_decimals(self, page):
        result = page.calculate(2.5, "multiply", 4.0)
        assert "Résultat: 10" in result

    def test_divide_decimals(self, page):
        result = page.calculate(7.5, "divide", 2.5)
        assert "Résultat: 3" in result

    # --- Tests avec nombres negatifs (Partie 5.1) ---

    def test_addition_negatives(self, page):
        result = page.calculate(-5, "add", -3)
        assert "Résultat: -8" in result

    def test_subtraction_negatives(self, page):
        result = page.calculate(-10, "subtract", 5)
        assert "Résultat: -15" in result

    def test_multiply_negatives(self, page):
        result = page.calculate(-4, "multiply", 3)
        assert "Résultat: -12" in result

    def test_divide_negatives(self, page):
        result = page.calculate(-10, "divide", 2)
        assert "Résultat: -5" in result

    # --- Tests UI (Partie 5.1) ---

    def test_title_displayed(self, driver):
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        h1 = driver.find_element(By.TAG_NAME, "h1")
        assert h1.is_displayed()
        assert h1.text == "Calculatrice Simple"

    def test_result_zone_style(self, driver):
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        result_div = driver.find_element(By.ID, "result")
        bg_color = result_div.value_of_css_property("background-color")
        assert bg_color in ["rgba(240, 240, 240, 1)", "rgb(240, 240, 240)"]

    def test_container_border_radius(self, driver):
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        container = driver.find_element(By.CLASS_NAME, "container")
        border_radius = container.value_of_css_property("border-radius")
        assert border_radius == "8px"

    def test_input_font_size(self, driver):
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        num1_input = driver.find_element(By.ID, "num1")
        font_size = num1_input.value_of_css_property("font-size")
        assert font_size == "16px"

    def test_button_is_full_width(self, driver):
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        button = driver.find_element(By.ID, "calculate")
        container = driver.find_element(By.CLASS_NAME, "container")

        button_width = button.size["width"]
        container_width = container.size["width"]

        assert button_width > container_width * 0.8