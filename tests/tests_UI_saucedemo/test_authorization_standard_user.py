import os
import allure
from allure_commons.types import Severity
from pages.authorization_page import AuthorizationPage
from pages.inventory_page import InventoryPage


@allure.severity(Severity.CRITICAL)
@allure.title("Авторизация")
@allure.suite("Позитивные тесты")
@allure.tag("UI", "REGRESS")
@allure.suite("All Items")
@allure.parent_suite("UI")
def test_authorization_standard_user():
    AuthorizationPage() \
        .open_authorization_page() \
        .fill_username(os.getenv("SAUCEDEMO_LOGIN")) \
        .fill_password(os.getenv("SAUCEDEMO_PASSWORD")) \
        .submit()

    InventoryPage().should_be_opened()
