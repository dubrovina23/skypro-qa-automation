
from selenium import webdriver

from lesson_07.pages.login_page import LoginPage
from lesson_07.pages.main_shop_page import MainShopPage
from lesson_07.pages.cart_page import CartPage
from lesson_07.pages.checkout_page import CheckoutPage


def test_shop_checkout_page_object() -> None:
    driver = webdriver.Firefox()
    total_text = ""

    products = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie",
    ]

    try:
        login_page = LoginPage(driver)
        main_page = MainShopPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)

        # Авторизация
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        # Добавление товаров в корзину
        for product in products:
            main_page.add_product(product)

        main_page.open_cart()

        # Проверка содержимого корзины
        actual_products = cart_page.get_product_names()
        assert sorted(actual_products) == sorted(products)

        # Оформление заказа
        cart_page.checkout()

        checkout_page.fill_customer_data(
            "Екатерина",
            "Тестовая",
            "123456"
        )
        checkout_page.continue_checkout()

        # Получение итоговой стоимости
        total_text = checkout_page.get_total()
        print("Итоговая стоимость:", total_text)

    finally:
        driver.quit()

    # Проверка после закрытия браузера
    assert total_text == "Total: $58.29", (
        f"Ожидалось $58.29, получено: {total_text}"
    )
