
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")

    CONTINUE_BUTTON = (
        By.CSS_SELECTOR,
        "[data-test='continue']"
    )

    TOTAL_LABEL = (
        By.CSS_SELECTOR,
        "[data-test='total-label']"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def fill_customer_data(
        self,
        first_name: str,
        last_name: str,
        postal_code: str
    ) -> None:
        fields = [
            (self.FIRST_NAME, first_name),
            (self.LAST_NAME, last_name),
            (self.POSTAL_CODE, postal_code),
        ]

        for locator, value in fields:
            field = self.wait.until(
                EC.visibility_of_element_located(locator)
            )
            field.send_keys(value)

    def continue_checkout(self) -> None:
        self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_BUTTON)
        ).click()

    def get_total(self) -> str:
        total_element = self.wait.until(
            EC.visibility_of_element_located(
                self.TOTAL_LABEL
            )
        )
        return total_element.text
