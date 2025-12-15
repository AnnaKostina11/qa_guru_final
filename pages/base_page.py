import logging
import os

import allure
from selene import browser, have, be
from selene.core.entity import Element, Collection
from selene.support.shared.jquery_style import s


class BasePage:
    def __init__(self) -> None:
        self.base_url = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com")
        self._config_logger()

    def _config_logger(self) -> None:
        self.logger = logging.getLogger(type(self).__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    # NAVIGATION

    def open_page(self, relative_url: str = "/") -> None:
        with allure.step(f"Open page: {relative_url}"):
            browser.config.base_url = self.base_url
            self.logger.info(f"Open {self.base_url}{relative_url}")
            browser.open(relative_url)

    def open_url(self, absolute_url: str) -> None:
        with allure.step(f"Open url: {absolute_url}"):
            self.logger.info(f"Open {absolute_url}")
            browser.open(absolute_url)

    # ACTIONS

    @allure.step("Выход из аккаунта (SauceDemo)")
    def logout(self) -> None:
        menu_button = s("#react-burger-menu-btn")
        logout_link = s("#logout_sidebar_link")

        with allure.step("Open burger menu"):
            menu_button.should(be.clickable).click()

        with allure.step("Click Logout"):
            logout_link.should(be.clickable).click()

    def click(self, element: Element, name: str = "element") -> None:
        with allure.step(f"Click: {name}"):
            element.should(be.clickable).click()

    def type(self, element: Element, text: str, name: str = "field", clear: bool = True) -> None:
        with allure.step(f"Type into {name}: {text}"):
            element.should(be.visible)
            if clear:
                element.clear()
            element.type(text)

    def press_enter(self, element: Element, name: str = "element") -> None:
        with allure.step(f"Press Enter: {name}"):
            element.should(be.visible).press_enter()

    def scroll_to(self, element: Element, name: str = "element") -> None:
        with allure.step(f"Scroll to: {name}"):
            element.should(be.present).scroll_to()

    # ASSERTIONS

    def should_be_visible(self, element: Element, name: str = "element") -> None:
        with allure.step(f"Should be visible: {name}"):
            element.should(be.visible)

    def should_be_hidden(self, element: Element, name: str = "element") -> None:
        with allure.step(f"Should be hidden: {name}"):
            element.should(be.hidden)

    def should_have_text(self, element: Element, text: str, name: str = "element") -> None:
        with allure.step(f"Should have text [{text}]: {name}"):
            element.should(have.text(text))

    def should_have_exact_text(self, element: Element, text: str, name: str = "element") -> None:
        with allure.step(f"Should have exact text [{text}]: {name}"):
            element.should(have.exact_text(text))

    def should_have_value(self, element: Element, value: str, name: str = "element") -> None:
        with allure.step(f"Should have value [{value}]: {name}"):
            element.should(have.value(value))

    def should_have_size(self, collection: Collection, size: int, name: str = "collection") -> None:
        with allure.step(f"Should have size {size}: {name}"):
            collection.should(have.size(size))

    def should_have_url(self, url: str) -> None:
        with allure.step(f"Should have url: {url}"):
            browser.should(have.url(url))

    def should_have_url_containing(self, partial: str) -> None:
        with allure.step(f"Should have url containing: {partial}"):
            browser.should(have.url_containing(partial))

    def should_have_title(self, title: str) -> None:
        with allure.step(f"Should have title: {title}"):
            browser.should(have.title(title))
