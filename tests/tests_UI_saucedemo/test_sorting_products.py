import os
import allure
from allure_commons.types import Severity

from pages.authorization_page import AuthorizationPage
from pages.inventory_page import InventoryPage


@allure.title("Сортировка товаров на главной странице")
@allure.severity(Severity.CRITICAL)
@allure.tag("UI", "REGRESS")
@allure.suite("Products")
@allure.parent_suite("UI")
def test_sorting_products(browser_setup):
    AuthorizationPage() \
        .open_authorization_page() \
        .fill_username(os.getenv("SAUCEDEMO_LOGIN")) \
        .fill_password(os.getenv("SAUCEDEMO_PASSWORD")) \
        .submit()

    inventory = InventoryPage().should_be_opened()

    initial_names = inventory.get_product_names()

    inventory.select_sort_option("az")
    assert inventory.get_product_names() == sorted(initial_names)

    inventory.select_sort_option("za")
    assert inventory.get_product_names() == sorted(initial_names, reverse=True)

    inventory.select_sort_option("lohi")
    prices_lohi = inventory.get_product_prices()
    assert prices_lohi == sorted(prices_lohi)

    inventory.select_sort_option("hilo")
    prices_hilo = inventory.get_product_prices()
    assert prices_hilo == sorted(prices_hilo, reverse=True)
