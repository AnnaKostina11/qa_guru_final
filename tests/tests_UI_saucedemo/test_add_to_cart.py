import allure
from allure_commons.types import Severity
from selene import browser
from pages.home_page import HomePage
from pages.authorization_page import AuthorizationPage
import os

@allure.title("Добавление в корзину")
@allure.severity(Severity.CRITICAL)
@allure.tag("UI", "REGRESS")
@allure.suite("All Items")
@allure.parent_suite("UI")
def test_add_to_shopping_cart(browser_setup, log_in_saucedemo):
    auth_page = AuthorizationPage(browser)

    auth_page.open_authorization_page()
    auth_page.fill_username(os.getenv("SAUCEDEMO_LOGIN"))
    auth_page.fill_password(os.getenv("SAUCEDEMO_PASSWORD"))
    auth_page.submit()

    home_page = HomePage(browser)

    home_page.add_product_to_shopping_cart_by_text("Sauce Labs Backpack")
    home_page.add_product_to_shopping_cart_by_text("Sauce Labs Bolt T-Shirt")

    home_page.verify_cart_badge_text("2")
