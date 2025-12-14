import os
import allure
import pytest

from pages.authorization_page import AuthorizationPage
from pages.inventory_page import InventoryPage


@allure.tag("UI")
@allure.suite("Authorization")
def test_authorization_standard_user():
    AuthorizationPage() \
        .open_authorization_page() \
        .fill_username(os.getenv("SAUCEDEMO_LOGIN")) \
        .fill_password(os.getenv("SAUCEDEMO_PASSWORD")) \
        .submit()

    InventoryPage().should_be_opened()
