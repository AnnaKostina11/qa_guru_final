import os

import allure
from allure_commons.types import Severity

from pages.authorization_page import AuthorizationPage
from pages.inventory_page import InventoryPage


@allure.epic("UI")
@allure.feature("Cart")
@allure.story("Add product")
class TestCartAdd:

    @allure.tag("UI", "REGRESS")
    @allure.label("layer", "ui")
    @allure.severity(Severity.CRITICAL)
    @allure.title("Добавление в корзину.")
    def test_add_to_shopping_cart(self, browser_setup):
        AuthorizationPage() \
            .open_authorization_page() \
            .fill_username(os.getenv("SAUCEDEMO_LOGIN")) \
            .fill_password(os.getenv("SAUCEDEMO_PASSWORD")) \
            .submit()

        inventory = InventoryPage().should_be_opened()
        inventory.add_product_to_shopping_cart_by_text("Sauce Labs Backpack")
        inventory.add_product_to_shopping_cart_by_text("Sauce Labs Bolt T-Shirt")
        inventory.verify_cart_badge_text("2")
