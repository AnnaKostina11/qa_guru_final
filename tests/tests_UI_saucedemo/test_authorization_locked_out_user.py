import allure
from allure_commons.types import Severity

from pages.authorization_page import AuthorizationPage
from pages.home_page import HomePage


@allure.title("Авторизация заблокированного пользователя")
@allure.severity(Severity.CRITICAL)
@allure.tag("UI", "REGRESS")
@allure.suite("Authorization")
@allure.parent_suite("UI")
def test_authorization_locked_out_user(manage_browser):
    browser = manage_browser
    auth_page = AuthorizationPage(browser)

    auth_page.open_authorization_page()
    auth_page.fill_username("locked_out_user")
    auth_page.fill_password("secret_sauce")
    auth_page.submit()

    # Проверяем, что остался на странице авторизации
    auth_page.verify_url()

    # Проверяем сообщение об ошибке
    auth_page.verify_locked_out_error_message()
