import allure
from allure_commons.types import Severity
from selene import browser
import os
from pages.authorization_page import AuthorizationPage
from pages.home_page import HomePage


@allure.title("Добавление в корзину")
@allure.severity(Severity.CRITICAL)
@allure.tag("UI", "REGRESS")
@allure.suite("All Items")
@allure.parent_suite("UI")
def test_add_to_shopping_cart(browser_setup, log_in_saucedemo):
    home_page = HomePage(browser)

    home_page.add_product_to_shopping_cart_by_text("Sauce Labs Backpack")
    home_page.add_product_to_shopping_cart_by_text("Sauce Labs Bolt T-Shirt")

    home_page.verify_cart_badge_text("2")
