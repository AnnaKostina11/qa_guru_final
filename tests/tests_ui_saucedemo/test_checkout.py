import os

import allure
from allure_commons.types import Severity

from pages.authorization_page import AuthorizationPage
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


@allure.epic("UI")
@allure.feature("Checkout")
@allure.story("Complete order")
class TestCheckout:

    @allure.tag("UI", "REGRESS")
    @allure.label("layer", "ui")
    @allure.severity(Severity.CRITICAL)
    @allure.title("Оформление заказа.")
    def test_buy_to_product(self, browser_setup, logged_in):
        inventory = logged_in

        inventory = InventoryPage().should_be_opened()
        inventory.add_product_to_shopping_cart_by_text("Sauce Labs Bike Light")
        inventory.open_cart()

        CartPage() \
            .should_be_cart_opened() \
            .go_to_checkout_step_one() \
            .fill_checkout_information(first_name="Anna", last_name="K", postal_code="22") \
            .go_to_checkout_step_two() \
            .finish_checkout() \
            .verify_complete_header()
