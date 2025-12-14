import os
import allure
from selene import browser, have, be
from selene.support.shared.jquery_style import s

from pages.base_page import BasePage


class AuthorizationPage(BasePage):
    login_logo = s(".login_logo")
    username_field = s("#user-name")
    password_field = s("#password")
    login_button = s("#login-button")
    error_container = s(".error-message-container")
    error_message = s(".error-message-container h3")

    @allure.step("Открытие страницы авторизации")
    def open_authorization_page(self) -> "AuthorizationPage":
        self.open_page("/")
        return self

    @allure.step("Ввод имени: {value}")
    def fill_username(self, value: str) -> "AuthorizationPage":
        self.type(self.username_field, value)
        return self

    @allure.step("Ввод пароля")
    def fill_password(self, value: str) -> "AuthorizationPage":
        self.type(self.password_field, value)
        return self

    @allure.step("Нажатие кнопки логина")
    def submit(self) -> "AuthorizationPage":
        self.click(self.login_button)
        return self

    # VERIFICATIONS

    @allure.step("Проверка title страницы")
    def verify_page_title(self) -> "AuthorizationPage":
        browser.should(have.title("Swag Labs"))
        return self

    @allure.step("Проверка URL страницы авторизации")
    def verify_url(self) -> "AuthorizationPage":
        base = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com").rstrip("/")
        browser.should(have.url(f"{base}/"))
        return self

    @allure.step("Проверка логотипа на странице логина")
    def verify_login_logo(self) -> "AuthorizationPage":
        self.login_logo.should(be.visible)
        return self

    @allure.step("Проверка сообщения об ошибке заблокированного пользователя")
    def verify_locked_out_error_message(self) -> "AuthorizationPage":
        self.error_message.should(have.text("Epic sadface: Sorry, this user has been locked out."))
        return self

    @allure.step("Проверка видимости сообщения об ошибке")
    def verify_error_message_visible(self) -> "AuthorizationPage":
        self.error_container.should(be.visible)
        return self
