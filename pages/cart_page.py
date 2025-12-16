import allure
from selene import be, have
from selene.core.entity import Element
from selene.support.shared.jquery_style import s

from pages.base_page import BasePage


class CartPage(BasePage):

    @property
    def title(self) -> Element:
        return s(".title")

    @property
    def checkout_button(self) -> Element:
        return s("#checkout")

    @property
    def first_name_field(self) -> Element:
        return s('[data-test="firstName"]')

    @property
    def last_name_field(self) -> Element:
        return s('[data-test="lastName"]')

    @property
    def postal_code_field(self) -> Element:
        return s('[data-test="postalCode"]')

    @property
    def continue_button(self) -> Element:
        return s('[data-test="continue"]')

    @property
    def finish_button(self) -> Element:
        return s('[data-test="finish"]')

    @property
    def complete_header(self) -> Element:
        return s('[data-test="complete-header"]')

    @allure.step("Проверка страницы корзины")
    def should_be_cart_opened(self) -> "CartPage":
        # Cart page: "Your Cart"
        self.title.should(have.exact_text("Your Cart"))
        return self

    @allure.step("Перейти к оформлению (Checkout step one)")
    def go_to_checkout_step_one(self) -> "CartPage":
        self.checkout_button.should(be.clickable).click()

        # Step one: "Checkout: Your Information"
        self.title.should(have.exact_text("Checkout: Your Information"))
        self.first_name_field.should(be.visible)
        return self

    @allure.step("Заполнить данные покупателя")
    def fill_checkout_information(self, first_name: str, last_name: str, postal_code: str) -> "CartPage":
        self.first_name_field.should(be.visible).clear().type(first_name)
        self.last_name_field.should(be.visible).clear().type(last_name)
        self.postal_code_field.should(be.visible).clear().type(postal_code)
        return self

    @allure.step("Нажатие Continue (Checkout step two)")
    def go_to_checkout_step_two(self) -> "CartPage":
        self.continue_button.should(be.clickable).click()

        self.title.should(have.exact_text("Checkout: Overview"))
        self.finish_button.should(be.visible)
        return self

    @allure.step("Завершение заказа (Finish)")
    def finish_checkout(self) -> "CartPage":
        self.finish_button.should(be.clickable).click()

        self.title.should(have.exact_text("Checkout: Complete!"))
        return self

    @allure.step("Проверка успешного завершения заказа")
    def verify_complete_header(self) -> "CartPage":
        self.complete_header.should(have.exact_text("Thank you for your order!"))
        return self
