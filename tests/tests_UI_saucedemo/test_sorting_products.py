import os
import allure
from allure_commons.types import Severity

from pages.authorization_page import AuthorizationPage
from pages.inventory_page import InventoryPage


@allure.title("Сортировка товаров по имени и цене")
@allure.severity(Severity.NORMAL)
@allure.tag("UI", "REGRESS")
@allure.suite("Products")
@allure.parent_suite("UI")
class TestSortingProducts:
    def test_sorting_products(self, browser_setup):
        # Логин
        AuthorizationPage() \
            .open_authorization_page() \
            .fill_username(os.getenv("SAUCEDEMO_LOGIN")) \
            .fill_password(os.getenv("SAUCEDEMO_PASSWORD")) \
            .submit()

        inventory = InventoryPage().should_be_opened()

        initial_names = inventory.get_product_names()

        inventory.select_sort_option("az")
        names_az = inventory.get_product_names()
        assert names_az == sorted(initial_names), "Сортировка по имени A→Z работает некорректно"

        inventory.select_sort_option("za")
        names_za = inventory.get_product_names()
        assert names_za == sorted(initial_names, reverse=True), "Сортировка по имени Z→A работает некорректно"

        inventory.select_sort_option("lohi")
        prices_lohi = inventory.get_product_prices()
        assert prices_lohi == sorted(prices_lohi), "Сортировка по цене Low→High работает некорректно"

        inventory.select_sort_option("hilo")
        prices_hilo = inventory.get_product_prices()
        assert prices_hilo == sorted(prices_hilo, reverse=True), "Сортировка по цене High→Low работает некорректно"
