import os

import allure
from allure_commons.types import Severity

from pages.authorization_page import AuthorizationPage


@allure.epic("UI")
@allure.feature("Authorization")
@allure.story("Negative login")
class TestAuthorizationNegative:

    @allure.tag("UI", "REGRESS")
    @allure.label("layer", "ui")
    @allure.severity(Severity.CRITICAL)
    @allure.title("Авторизация негативная.")
    def test_authorization_locked_out_user(self, browser_setup):
        AuthorizationPage() \
            .open_authorization_page() \
            .fill_username(os.getenv("SAUCEDEMO_LOGIN_FAIL")) \
            .fill_password(os.getenv("SAUCEDEMO_PASSWORD")) \
            .submit() \
            .verify_error_message_visible() \
            .verify_locked_out_error_message()
