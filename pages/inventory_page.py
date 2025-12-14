import allure
from selene import have, be
from selene.support.shared.jquery_style import s, ss

from pages.base_page import BasePage


class InventoryPage(BasePage):
    title = s(".title")
    cart_badge = s(".shopping_cart_badge")
    cart_link = s(".shopping_cart_link")
    items = ss(".inventory_item")

    sort_select = s(".product_sort_container")
    product_names = ss(".inventory_item_name")
    product_prices = ss(".inventory_item_price")

    @allure.step("Проверка, что открыта страница каталога")
    def should_be_opened(self) -> "InventoryPage":
        self.title.should(have.exact_text("Products"))
        return self

    @allure.step("Добавить в корзину товар: {text}")
    def add_product_to_shopping_cart_by_text(self, text: str) -> "InventoryPage":
        item = self.items.by(have.text(text)).first
        item.element("button.btn_inventory").should(be.clickable).click()
        return self

    @allure.step("Удалить из корзины товар: {text}")
    def remove_product_from_cart_by_text(self, text: str) -> "InventoryPage":
        item = self.items.by(have.text(text)).first
        item.element("button.btn_inventory").should(be.clickable).click()
        return self

    @allure.step("Проверка бейджа корзины: {value}")
    def verify_cart_badge_text(self, value: str) -> "InventoryPage":
        self.cart_badge.should(be.visible).should(have.exact_text(value))
        return self

    @allure.step("Проверка, что бейдж корзины не виден")
    def verify_cart_badge_not_visible(self) -> "InventoryPage":
        self.cart_badge.should(be.hidden)
        return self

    @allure.step("Открыть корзину")
    def open_cart(self) -> None:
        self.cart_link.should(be.clickable).click()

    @allure.step("Выбор сортировки: {value}")
    def select_sort_option(self, value: str) -> "InventoryPage":
        self.sort_select.should(be.visible).select_option_by_value(value)
        self.sort_select.should(have.value(value))
        return self

    @allure.step("Получить список названий товаров")
    def get_product_names(self) -> list[str]:
        return [e.get(query=lambda el: el().text) for e in self.product_names]

    @allure.step("Получить список цен товаров")
    def get_product_prices(self) -> list[float]:
        prices = [e.get(query=lambda el: el().text) for e in self.product_prices]
        return [float(p.replace("$", "").strip()) for p in prices]
