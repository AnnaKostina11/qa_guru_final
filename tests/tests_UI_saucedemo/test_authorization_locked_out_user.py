import allure
from allure_commons.types import Severity
import os
from pages.authorization_page import AuthorizationPage
from pages.home_page import HomePage


@allure.title("Авторизация заблокированного пользователя")
@allure.severity(Severity.CRITICAL)
@allure.tag("UI", "REGRESS")
@allure.suite("Authorization")
@allure.parent_suite("UI")
def test_authorization_locked_out_user(browser_setup):
    browser = browser_setup
    auth_page = AuthorizationPage(browser)

    auth_page.open_authorization_page()
    auth_page.fill_username(os.getenv("SAUCEDEMO_LOGIN_FAIL"))
    auth_page.fill_password(os.getenv("SAUCEDEMO_PASSWORD"))
    auth_page.submit()

    # Проверяем, что остался на странице авторизации
    auth_page.verify_url()

    # Проверяем сообщение об ошибке
    auth_page.verify_locked_out_error_message()
