import allure
from allure_commons.types import Severity

from pages.inventory_page import InventoryPage


@allure.epic("UI")
@allure.feature("Authorization")
@allure.story("Positive login")
class TestAuthorizationPositive:

    @allure.tag("UI", "REGRESS")
    @allure.label("layer", "ui")
    @allure.severity(Severity.CRITICAL)
    @allure.title("Авторизация позитивная.")
    def test_authorization_standard_user(self, browser_setup, logged_in):
        inventory = logged_in

        InventoryPage().should_be_opened()
