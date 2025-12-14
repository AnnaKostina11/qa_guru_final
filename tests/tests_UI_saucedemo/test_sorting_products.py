import allure
from allure_commons.types import Severity

from pages.authorization_page import AuthorizationPage
from pages.home_page import HomePage
import config


@allure.title("Сортировка товаров по имени и цене")
@allure.severity(Severity.NORMAL)
@allure.tag("UI", "REGRESS")
@allure.suite("Products")
@allure.parent_suite("UI")
class TestSortingProducts:

    def test_sorting_products(self, browser_setup):
        browser = browser_setup
        # Логин
        auth_page = AuthorizationPage(browser)
        auth_page.open_authorization_page()
        auth_page.fill_username(config.SAUCEDEMO_LOGIN)
        auth_page.fill_password(config.SAUCEDEMO_PASSWORD)
        auth_page.submit()

        home_page = HomePage(browser)
        home_page.verify_url()

        # Исходные имена
        initial_names = home_page.get_product_names()

        # A -> Z
        home_page.select_sort_option("az")
        names_az = home_page.get_product_names()
        assert names_az == sorted(initial_names), "Сортировка по имени A→Z работает некорректно"

        # Z -> A
        home_page.select_sort_option("za")
        names_za = home_page.get_product_names()
        assert names_za == sorted(initial_names, reverse=True), "Сортировка по имени Z→A работает некорректно"

        # Price Low -> High
        home_page.select_sort_option("lohi")
        prices_lohi = home_page.get_product_prices()
        assert prices_lohi == sorted(prices_lohi), "Сортировка по цене Low→High работает некорректно"

        # Price High -> Low
        home_page.select_sort_option("hilo")
        prices_hilo = home_page.get_product_prices()
        assert prices_hilo == sorted(prices_hilo, reverse=True), "Сортировка по цене High→Low работает некорректно"
