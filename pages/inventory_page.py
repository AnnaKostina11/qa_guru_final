import allure
from selene import have, be
from selene.support.shared.jquery_style import s, ss

from pages.base_page import BasePage


class InventoryPage(BasePage):
    title = s(".title")
    cart_badge = s(".shopping_cart_badge")
    cart_link = s(".shopping_cart_link")
    items = ss(".inventory_item")

    @allure.step("Проверка, что открыта страница каталога")
    def should_be_opened(self) -> "InventoryPage":
        self.title.should(have.text("Products"))
        return self

    @allure.step("Добавить первый товар в корзину")
    def add_first_item_to_cart(self) -> "InventoryPage":
        self.items.first.element(".btn_inventory").should(be.clickable).click()
        return self

    @allure.step("Открыть корзину")
    def open_cart(self) -> None:
        self.cart_link.should(be.clickable).click()
