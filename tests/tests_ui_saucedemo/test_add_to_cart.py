import os

import allure
from allure_commons.types import Severity

from pages.inventory_page import InventoryPage


@allure.epic("UI")
@allure.feature("Cart")
@allure.story("Add product")
class TestCartAdd:

    @allure.tag("UI", "REGRESS")
    @allure.label("layer", "ui")
    @allure.severity(Severity.CRITICAL)
    @allure.title("Добавление в корзину.")
    def test_add_to_shopping_cart(self, browser_setup, logged_in):
        inventory = logged_in

        inventory = InventoryPage().should_be_opened()
        inventory.add_product_to_shopping_cart_by_text("Sauce Labs Backpack")
        inventory.add_product_to_shopping_cart_by_text("Sauce Labs Bolt T-Shirt")
        inventory.verify_cart_badge_text("2")
