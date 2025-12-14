import os
import allure
from allure_commons.types import Severity

from pages.authorization_page import AuthorizationPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@allure.title("Оформление заказа")
@allure.severity(Severity.CRITICAL)
@allure.tag("UI", "REGRESS")
@allure.suite("Позитивные тесты")
@allure.parent_suite("Тесты UI")
def test_buy_to_product(browser_setup):
    # Логин
    AuthorizationPage() \
        .open_authorization_page() \
        .fill_username(os.getenv("SAUCEDEMO_LOGIN")) \
        .fill_password(os.getenv("SAUCEDEMO_PASSWORD")) \
        .submit()

    # Добавление товара в корзину
    inventory = InventoryPage().should_be_opened()
    inventory.add_product_to_shopping_cart_by_text("Sauce Labs Bike Light")
    inventory.open_cart()

    # Оформление заказа
    cart = CartPage()
    cart.click_checkout_button()
    cart.fill_first_name("Anna")
    cart.fill_last_name("K")
    cart.fill_postal_code("22")
    cart.click_continue_button()
    cart.click_finish_button()
    cart.verify_complete_header()
