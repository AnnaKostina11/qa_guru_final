import os

import allure
from allure_commons.types import Severity

from pages.authorization_page import AuthorizationPage
from pages.inventory_page import InventoryPage


@allure.severity(Severity.CRITICAL)
@allure.title("Удаление товара из корзины.")
@allure.suite("Позитивные тесты")
@allure.tag("UI", "REGRESS")
@allure.suite("All Items")
@allure.parent_suite("UI")
def test_remove_from_cart(browser_setup):
    # Логин
    AuthorizationPage() \
        .open_authorization_page() \
        .fill_username(os.getenv("SAUCEDEMO_LOGIN")) \
        .fill_password(os.getenv("SAUCEDEMO_PASSWORD")) \
        .submit()
    inventory = InventoryPage().should_be_opened()
    inventory.add_product_to_shopping_cart_by_text("Sauce Labs Backpack")
    inventory.verify_cart_badge_text("1")
    # удаление: на inventory кнопка станет Remove (селектор остаётся btn_inventory)
    inventory.remove_product_from_cart_by_text("Sauce Labs Backpack")
    inventory.verify_cart_badge_not_visible()
