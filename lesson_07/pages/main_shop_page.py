
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainShopPage:
    PRODUCT_BUTTONS = {
        "Sauce Labs Backpack": (
            By.CSS_SELECTOR,
            "[data-test='add-to-cart-sauce-labs-backpack']"
        ),
        "Sauce Labs Bolt T-Shirt": (
            By.CSS_SELECTOR,
            "[data-test='add-to-cart-sauce-labs-bolt-t-shirt']"
        ),
        "Sauce Labs Onesie": (
            By.CSS_SELECTOR,
            "[data-test='add-to-cart-sauce-labs-onesie']"
        ),
    }

    CART_LINK = (
        By.CSS_SELECTOR,
        "[data-test='shopping-cart-link']"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def add_product(self, product_name: str) -> None:
        locator = self.PRODUCT_BUTTONS[product_name]
        button = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        button.click()

    def open_cart(self) -> None:
        self.wait.until(
            EC.element_to_be_clickable(self.CART_LINK)
        ).click()
