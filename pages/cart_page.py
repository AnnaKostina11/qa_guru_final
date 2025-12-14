import allure
from selene import have, be
from selene.support.shared.jquery_style import s

from pages.base_page import BasePage


class CartPage(BasePage):
    title = s(".title")
    cart_items = s(".cart_list")
    checkout_button = s('[data-test="checkout"]')

    # Checkout step 1 (информация)
    first_name_field = s('[data-test="first-name"]')
    last_name_field = s('[data-test="last-name"]')
    postal_code_field = s('[data-test="postal-code"]')
    continue_button = s('[data-test="continue"]')

    # Checkout step 2 (overview)
    finish_button = s('[data-test="finish"]')

    # Complete page
    complete_header = s('[data-test="complete-header"]')

    @allure.step("Проверка страницы корзины")
    def should_be_opened(self) -> "CartPage":
        self.title.should(have.text("Your Cart"))
        return self

    @allure.step("Перейти к оформлению")
    def click_checkout_button(self) -> "CartPage":
        self.checkout_button.should(be.clickable).click()
        return self

    @allure.step("Ввод имени: {value}")
    def fill_first_name(self, value: str) -> "CartPage":
        self.first_name_field.should(be.visible).type(value)
        return self

    @allure.step("Ввод фамилии: {value}")
    def fill_last_name(self, value: str) -> "CartPage":
        self.last_name_field.should(be.visible).type(value)
        return self

    @allure.step("Ввод почтового индекса: {value}")
    def fill_postal_code(self, value: str) -> "CartPage":
        self.postal_code_field.should(be.visible).type(value)
        return self

    @allure.step("Нажатие Continue")
    def click_continue_button(self) -> "CartPage":
        self.continue_button.should(be.clickable).click()
        return self

    @allure.step("Завершение заказа")
    def click_finish_button(self) -> "CartPage":
        self.finish_button.should(be.clickable).click()
        return self

    @allure.step("Проверка заголовка успешного завершения")
    def verify_complete_header(self) -> "CartPage":
        self.complete_header.should(have.exact_text("Thank you for your order!"))
        return self
