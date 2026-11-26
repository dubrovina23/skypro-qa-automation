
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    PRODUCT_NAMES = (
        By.CSS_SELECTOR,
        ".inventory_item_name"
    )

    CHECKOUT_BUTTON = (
        By.CSS_SELECTOR,
        "[data-test='checkout']"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def get_product_names(self) -> list[str]:
        elements = self.wait.until(
            EC.visibility_of_all_elements_located(
                self.PRODUCT_NAMES
            )
        )
        return [element.text for element in elements]

    def checkout(self) -> None:
        self.wait.until(
            EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
        ).click()
