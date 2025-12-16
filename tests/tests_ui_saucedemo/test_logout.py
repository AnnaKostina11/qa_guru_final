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
    def test_logout(self, logged_in):
        inventory = logged_in

        inventory.logout()

        AuthorizationPage() \
            .verify_url() \
            .verify_page_title() \
            .verify_login_logo()
