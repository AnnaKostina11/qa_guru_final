import os

import allure
from allure_commons.types import Severity

from pages.authorization_page import AuthorizationPage
from pages.inventory_page import InventoryPage


@allure.epic("UI")
@allure.feature("Cart")
@allure.story("Remove product")
class TestCartRemove:

    @allure.tag("UI", "REGRESS")
    @allure.label("layer", "ui")
    @allure.severity(Severity.CRITICAL)
    @allure.title("Удаление товара из корзины.")
    def test_remove_from_cart(self, browser_setup, logged_in):
        inventory = logged_in

        inventory = InventoryPage().should_be_opened()
        inventory.add_product_to_shopping_cart_by_text("Sauce Labs Backpack")
        inventory.verify_cart_badge_text("1")
        inventory.remove_product_from_cart_by_text("Sauce Labs Backpack")
        inventory.verify_cart_badge_not_visible()
