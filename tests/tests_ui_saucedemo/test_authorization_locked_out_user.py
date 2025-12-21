import allure
from allure_commons.types import Severity


@allure.epic("UI")
@allure.feature("Authorization")
@allure.story("Negative login")
class TestAuthorizationNegative:

    @allure.tag("UI", "REGRESS")
    @allure.label("layer", "ui")
    @allure.severity(Severity.CRITICAL)
    @allure.title("Авторизация негативная.")
    def test_authorization_locked_out_user(self, browser_setup, logged_in):
        inventory = logged_in
