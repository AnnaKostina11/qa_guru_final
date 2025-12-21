import allure
from allure_commons.types import Severity


@allure.epic("UI")
@allure.feature("Catalog")
@allure.story("Sorting")
class TestCatalogSorting:

    @allure.tag("UI", "REGRESS")
    @allure.label("layer", "ui")
    @allure.severity(Severity.CRITICAL)
    @allure.title("Сортировка товаров на главной странице")
    def test_sorting_products(self, logged_in):
        inventory = logged_in

        initial_names = inventory.get_product_names()
        expected_az = sorted(initial_names)
        expected_za = sorted(initial_names, reverse=True)

        inventory.select_sort_option("az")
        assert inventory.get_product_names() == expected_az

        inventory.select_sort_option("za")
        assert inventory.get_product_names() == expected_za

        inventory.select_sort_option("lohi")
        actual_lohi = inventory.get_product_prices()
        assert actual_lohi == sorted(actual_lohi)

        inventory.select_sort_option("hilo")
        actual_hilo = inventory.get_product_prices()
        assert actual_hilo == sorted(actual_hilo, reverse=True)
