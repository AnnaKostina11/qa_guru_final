import allure
from selene import have, be
from selene.support.shared.jquery_style import s, ss

from pages.base_page import BasePage


class CartPage(BasePage):
    title = s(".title")
    cart_items = ss(".cart_item")
    checkout_button = s("#checkout")
    continue_shopping_button = s("#continue-shopping")

    @allure.step("Проверка страницы корзины")
    def should_be_opened(self) -> "CartPage":
        self.title.should(have.text("Your Cart"))
        return self

    @allure.step("Проверка, что в корзине {count} товар(ов)")
    def should_have_items(self, count: int) -> "CartPage":
        self.cart_items.should(have.size(count))
        return self

    @allure.step("Перейти к оформлению")
    def checkout(self) -> None:
        self.checkout_button.should(be.clickable).click()
