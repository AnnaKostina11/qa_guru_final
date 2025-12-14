import logging
import config
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, browser: WebDriver) -> None:
        self.browser = browser
        self.base_url = config.SAUCEDEMO_URL
        self.__config_logger()

    # CONFIG LOGGER
    def __config_logger(self) -> None:
        self.logger = logging.getLogger(type(self).__name__)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    # OPEN PAGE
    def open_page(self, url: str) -> None:
        self.logger.info(f"Open {self.base_url + url}")
        self.browser.get(self.base_url + url)

    # BASE ACTIONS
    def click_on_element(self, locator: tuple[str, str], timeout: float = 3.0) -> None:
        self.logger.info(f"Click on the element {locator}")
        try:
            webelement = WebDriverWait(self.browser, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            ActionChains(self.browser).move_to_element(webelement).pause(
                0.5
            ).click().perform()
        except TimeoutException:
            self.logger.error(f"Failed click on the element {locator}")
            raise AssertionError(
                f"Ошибка клика на элемента {locator} в течение {timeout} сек."
            )

    def type_text_into_element(
        self,
        locator: tuple[str, str],
        text: str,
        timeout: float = 3.0,
    ) -> None:
        self.logger.info(f"Type '{text}' into element {locator}")
        try:
            webelement = WebDriverWait(self.browser, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            ActionChains(self.browser).move_to_element(webelement).pause(
                0.5
            ).click().perform()
            webelement.clear()
            for letter in text:
                webelement.send_keys(letter)
        except TimeoutException:
            self.logger.error(f"Failed type text into element {locator}")
            raise AssertionError(
                f"Ошибка ввода текста в элемент {locator} в течение {timeout} сек."
            )

    # BASE ASSERTIONS
    def assert_that_element_is_visible(
        self,
        locator: tuple[str, str],
        timeout: float = 3.0,
    ) -> None:
        self.logger.info(f"Search the element with locator {locator}")
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.error(f"Failed to found element {locator}")
            raise AssertionError(
                f"Элемент с локатором {locator} не обнаружен в течение {timeout} сек."
            )

    def assert_that_page_have_title(self, title: str, timeout: float = 3.0) -> None:
        self.logger.info(f"Search page title '{title}'")
        try:
            WebDriverWait(self.browser, timeout).until(EC.title_is(title))
        except TimeoutException:
            self.logger.error(f"Title not '{title}'")
            raise AssertionError(f"Title страницы не '{title}'.")

    def assert_that_url_contains(self, url: str, timeout: float = 3.0) -> None:
        self.logger.info(f"Check page URL")
        try:
            WebDriverWait(self.browser, timeout).until(EC.url_contains(url))
        except TimeoutException:
            self.logger.error(f"URL doesn't contain '{url}'")
            raise AssertionError(f"URL не содержит '{url}'.")

    def assert_that_element_have_text(
        self, locator: tuple[str, str], text: str, timeout: float = 3.0
    ) -> None:
        self.logger.info(f"Search text '{text}' into element {locator}")
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
        except TimeoutException:
            self.logger.error(f"Element {locator} haven't text '{text}'")
            raise AssertionError(f"Элемент {locator} не содержит текст '{text}'")

    def assert_that_count_of_elements_equal(
        self,
        locator: tuple[str, str],
        count: int,
        timeout: float = 3.0,
    ) -> None:
        self.logger.info(f"Search {count} elements {locator}")
        try:
            WebDriverWait(self.browser, timeout).until(
                count_of_elements_equal(locator, count)
            )
        except TimeoutException:
            self.logger.error(f"Failed to find {count} elements {locator}")
            raise AssertionError(f"Не удалось найти {count} элементов {locator}")