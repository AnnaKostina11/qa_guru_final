import os

import allure
from allure_commons.types import Severity

from pages.authorization_page import AuthorizationPage
from pages.inventory_page import InventoryPage


@allure.epic("UI")
@allure.feature("Authorization")
@allure.story("Positive login")
class TestAuthorizationPositive:

    @allure.tag("UI", "REGRESS")
    @allure.label("layer", "ui")
    @allure.severity(Severity.CRITICAL)
    @allure.title("Авторизация позитивная.")
    def test_authorization_standard_user(self, browser_setup):
        AuthorizationPage() \
            .open_authorization_page() \
            .fill_username(os.getenv("SAUCEDEMO_LOGIN")) \
            .fill_password(os.getenv("SAUCEDEMO_PASSWORD")) \
            .submit()

        InventoryPage().should_be_opened()
