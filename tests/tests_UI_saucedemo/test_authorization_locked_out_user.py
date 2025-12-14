import os
import allure

from pages.authorization_page import AuthorizationPage


@allure.tag("UI")
@allure.suite("Authorization")
def test_authorization_locked_out_user():
    AuthorizationPage() \
        .open_authorization_page() \
        .fill_username(os.getenv("SAUCEDEMO_LOGIN_FAIL")) \
        .fill_password(os.getenv("SAUCEDEMO_PASSWORD")) \
        .submit() \
        .verify_error_message_visible() \
        .verify_locked_out_error_message()
