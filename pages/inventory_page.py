import allure
from selene import have, be
from selene.support.shared.jquery_style import s, ss

from pages.base_page import BasePage


class InventoryPage(BasePage):
    sort_select = s(".product_sort_container")
    product_names = ss(".inventory_item_name")
    product_prices = ss(".inventory_item_price")

    @allure.step("Проверка, что открыта страница каталога")
    def should_be_opened(self) -> "InventoryPage":
        s(".title").should(have.exact_text("Products"))
        return self

    @allure.step("Выбор сортировки: {value}")
    def select_sort_option(self, value: str) -> "InventoryPage":
        # для <select> в Selene работает select_option_by_value
        self.sort_select.should(be.visible).select_option_by_value(value)
        self.sort_select.should(have.value(value))
        return self

    @allure.step("Получить список названий товаров")
    def get_product_names(self) -> list[str]:
        return [el.get(query="text") for el in self.product_names]  # эквивалент .texts(), но явнее

    @allure.step("Получить список цен товаров")
    def get_product_prices(self) -> list[float]:
        prices_raw = [el.get(query="text") for el in self.product_prices]
        # "$9.99" -> 9.99
        return [float(p.replace("$", "").strip()) for p in prices_raw]
