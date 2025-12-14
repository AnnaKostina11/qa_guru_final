import logging
import os

import allure
from selene import browser, have, be
from selene.core.entity import Element
from selene.core.wait import Command


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

    def open_page(self, relative_url: str = "/") -> None:
        with allure.step(f"Open {relative_url}"):
            self.logger.info(f"Open {self.base_url}{relative_url}")
            browser.config.base_url = self.base_url
            browser.open(relative_url)

    def click(self, element: Element) -> None:
        element.should(be.clickable).click()

    def type(self, element: Element, text: str) -> None:
        element.should(be.visible).clear().type(text)

    def should_have_text(self, element: Element, text: str) -> None:
        element.should(have.text(text))

    def should_be_visible(self, element: Element) -> None:
        element.should(be.visible)

    def should_have_url(self, url: str) -> None:
        browser.should(have.url(url))

    def should_have_title(self, title: str) -> None:
        browser.should(have.title(title))
