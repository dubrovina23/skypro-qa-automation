
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    URL = (
        "https://bonigarcia.dev/"
        "selenium-webdriver-java/slow-calculator.html"
    )

    DELAY_FIELD = (By.CSS_SELECTOR, "#delay")
    SCREEN = (By.CLASS_NAME, "screen")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self) -> None:
        self.driver.get(self.URL)

    def set_delay(self, seconds: int) -> None:
        field = self.wait.until(
            EC.visibility_of_element_located(self.DELAY_FIELD)
        )
        field.clear()
        field.send_keys(str(seconds))

    def press_button(self, button_text: str) -> None:
        locator = (
            By.XPATH,
            f"//span[normalize-space()='{button_text}']"
        )
        button = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        button.click()

    def get_result(self, expected_text: str) -> str:
        WebDriverWait(self.driver, 60).until(
            EC.text_to_be_present_in_element(
                self.SCREEN, expected_text
            )
        )
        screen = self.driver.find_element(*self.SCREEN)
        return screen.text
