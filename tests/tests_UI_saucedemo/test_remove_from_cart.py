import allure
from allure_commons.types import Severity

from pages.home_page import HomePage
from pages.authorization_page import AuthorizationPage
import config


@allure.title("Удаление товара из корзины")
@allure.severity(Severity.CRITICAL)
@allure.tag("UI", "REGRESS")
@allure.suite("Shopping Cart")
@allure.parent_suite("UI")
class TestShoppingCart:
    def test_remove_from_cart(self, browser):
        # Логин
        auth_page = AuthorizationPage(browser)
        auth_page.open_authorization_page()
        auth_page.fill_username(config.SAUCEDEMO_LOGIN)
        auth_page.fill_password(config.SAUCEDEMO_PASSWORD)
        auth_page.submit()

        home_page = HomePage(browser)
        home_page.add_product_to_shopping_cart_by_text("Sauce Labs Backpack")
        home_page.verify_cart_badge_text("1")

        home_page.remove_product_from_cart_by_text("Sauce Labs Backpack")

        home_page.verify_cart_badge_not_visible()