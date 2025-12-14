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
def test_authorization(browser_setup):
    browser = browser_setup
    home_page = HomePage(browser)
    auth_page = AuthorizationPage(browser)
    auth_page.open_authorization_page()
    auth_page.fill_username(os.getenv("SAUCEDEMO_LOGIN"))
    auth_page.fill_password(os.getenv("SAUCEDEMO_PASSWORD"))
    auth_page.submit()
    home_page.verify_url()
