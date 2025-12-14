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
        self.title.should(have.exact_text("Products"))
        return self

    @allure.step("Добавить в корзину товар: {text}")
    def add_product_to_shopping_cart_by_text(self, text: str) -> "InventoryPage":
        # Находим карточку товара по тексту (внутри .inventory_item обычно есть имя/описание)
        item = self.items.by(have.text(text)).first
        # Внутри карточки жмём кнопку Add to cart (класс у кнопки обычно btn_inventory)
        item.element("button.btn_inventory").should(be.clickable).click()
        return self

    @allure.step("Проверка бейджа корзины: {value}")
    def verify_cart_badge_text(self, value: str) -> "InventoryPage":
        self.cart_badge.should(be.visible).should(have.exact_text(value))
        return self

    @allure.step("Открыть корзину")
    def open_cart(self) -> None:
        self.cart_link.should(be.clickable).click()
