
from selenium import webdriver
from lesson_07.pages.calculator_page import CalculatorPage


def test_slow_calculator_page_object() -> None:
    driver = webdriver.Chrome()

    try:
        calculator = CalculatorPage(driver)

        calculator.open()
        calculator.set_delay(45)

        calculator.press_button("7")
        calculator.press_button("+")
        calculator.press_button("8")
        calculator.press_button("=")

        result = calculator.get_result("15")

        assert result == "15"

    finally:
        driver.quit()
