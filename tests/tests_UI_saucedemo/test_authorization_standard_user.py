import allure
import config
from allure_commons.types import Severity
from pages.authorization_page import AuthorizationPage
from pages.home_page import HomePage

@allure.id('01_authorization_standard_user')
@allure.tag('UI', 'user_authorization')
@allure.title("Проверка авторизации standard_user")
@allure.severity(Severity.CRITICAL)
@allure.parent_suite('UI')
@allure.suite('user_authorization')
def test_authorization(browser):
    auth = AuthorizationPage(browser)
    home = HomePage(browser)
    auth.open_authorization_page()
    auth.fill_username(config.SAUCEDEMO_LOGIN)
    auth.fill_password(config.SAUCEDEMO_PASSWORD)
    auth.submit()
    home.verify_url()
