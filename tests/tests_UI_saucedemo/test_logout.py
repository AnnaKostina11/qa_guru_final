import allure
from allure_commons.types import Severity

from pages.home_page import HomePage
from pages.authorization_page import AuthorizationPage
import config


@allure.title("Выход из аккаунта")
@allure.severity(Severity.CRITICAL)
@allure.tag("UI", "REGRESS")
@allure.suite("Authorization")
@allure.parent_suite("UI")
class TestAuthorization:
    def test_logout(self, browser_setup):
        browser = browser_setup
        """
        Проверяет корректный выход из аккаунта
        Ожидается: возврат на страницу авторизации
        """
        # Логин
        auth_page = AuthorizationPage(browser)
        auth_page.open_authorization_page()
        auth_page.fill_username(config.SAUCEDEMO_LOGIN)
        auth_page.fill_password(config.SAUCEDEMO_PASSWORD)
        auth_page.submit()

        # Выход
        home_page = HomePage(browser)
        home_page.logout()

        # Проверки
        auth_page.verify_url()
        auth_page.verify_page_title()
        auth_page.verify_login_logo()
