import os

import allure
from allure_commons.types import Severity

from pages.authorization_page import AuthorizationPage


@allure.epic("UI")
@allure.feature("Authorization")
@allure.story("Logout")
class TestAuthorizationLogout:

    @allure.tag("UI", "REGRESS")
    @allure.label("layer", "ui")
    @allure.severity(Severity.CRITICAL)
    @allure.title("Выход из аккаунта.")
    def test_logout(self, browser_setup):
        auth_page = (
            AuthorizationPage()
            .open_authorization_page()
            .fill_username(os.getenv("SAUCEDEMO_LOGIN"))
            .fill_password(os.getenv("SAUCEDEMO_PASSWORD"))
            .submit()
        )

        auth_page.logout()
        auth_page.verify_url()
        auth_page.verify_page_title()
        auth_page.verify_login_logo()
