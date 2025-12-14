import os
import allure
from allure_commons.types import Severity

from pages.authorization_page import AuthorizationPage

@allure.severity(Severity.CRITICAL)
@allure.title("Выход из аккаунта")
@allure.suite("Позитивные тесты")
@allure.tag("UI", "REGRESS")
@allure.suite("All Items")
@allure.parent_suite("UI")
class TestAuthorization:
    def test_logout(self, browser_setup):
        auth_page = AuthorizationPage() \
            .open_authorization_page() \
            .fill_username(os.getenv("SAUCEDEMO_LOGIN")) \
            .fill_password(os.getenv("SAUCEDEMO_PASSWORD")) \
            .submit()

        # logout доступен из BasePage, поэтому можно вызвать прямо отсюда
        auth_page.logout()

        auth_page.verify_url()
        auth_page.verify_page_title()
        auth_page.verify_login_logo()
