import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class HomePage(BasePage):
    APP_LOGO = By.CSS_SELECTOR, ".app_logo"
    SHOPPING_CART_LINK = By.CSS_SELECTOR, "[data-test=shopping-cart-link]"
    SECONDARY_HEADER = By.CSS_SELECTOR, "[data-test=secondary-header]"
    INVENTORY_LIST = By.CSS_SELECTOR, "[data-test=inventory-list]"
    FOOTER = By.CSS_SELECTOR, "[data-test=footer]"
    SHOPPING_CART_BADGE = By.CSS_SELECTOR, "[data-test=shopping-cart-badge]"
    _INVENTORY_ITEM_LABEL = (
        By.XPATH,
        "//div[contains(@class, 'inventory_item_label')]"
    )

    # Меню и выход
    LOGOUT_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_MENU_ITEM = (By.ID, "logout_sidebar_link")

    # Локатор для кнопки Remove (шаблон)
    _INVENTORY_ITEM_REMOVE_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'inventory_item_label') and contains(., '{text}')]"
        "/following-sibling::div/button[contains(., 'Remove')]"
    )

    # Локаторы для сортировки и товаров
    SORT_SELECT = (By.CSS_SELECTOR, "[data-test=product-sort-container]")  # [web:79]
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")                    # [web:62]
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")                  # [web:42]

    # ACTIONS
    @allure.step("Добавление в корзину товара {text}")
    def add_product_to_shopping_cart_by_text(self, text: str) -> "HomePage":
        add_locator = (
            By.XPATH,
            f"{self._INVENTORY_ITEM_LABEL[1]}[contains(., '{text}')]"
            f"/following-sibling::div/button[contains(., 'Add to cart')]"
        )
        self.click_on_element(add_locator)
        return self

    @allure.step("Нажатие на ссылку корзины")
    def click_on_shopping_cart_link(self) -> "HomePage":
        self.click_on_element(self.SHOPPING_CART_LINK)
        return self

    @allure.step("Выход из аккаунта")
    def logout(self) -> "HomePage":
        self.click_on_element(self.LOGOUT_BUTTON)
        self.click_on_element(self.LOGOUT_MENU_ITEM)
        return self

    @allure.step("Удаление из корзины товара {text}")
    def remove_product_from_cart_by_text(self, text: str) -> "HomePage":
        remove_locator = (
            By.XPATH,
            self._INVENTORY_ITEM_REMOVE_BUTTON[1].format(text=text)
        )
        self.click_on_element(remove_locator)
        return self

    # VERIFICATION
    @allure.step("Проверка URL страницы")
    def verify_url(self) -> "HomePage":
        self.assert_that_url_contains("inventory")
        return self

    @allure.step("Проверка title страницы")
    def verify_page_title(self) -> "HomePage":
        self.assert_that_page_have_title("Swag Labs")
        return self

    @allure.step("Проверка логотипа страницы")
    def verify_app_logo(self) -> "HomePage":
        self.assert_that_element_have_text(self.APP_LOGO, "Swag Labs")
        return self

    @allure.step("Проверка наличия ссылки на корзину")
    def verify_shopping_cart_link(self) -> "HomePage":
        self.assert_that_element_is_visible(self.SHOPPING_CART_LINK)
        return self

    @allure.step("Проверка второго заголовка")
    def verify_secondary_header(self) -> "HomePage":
        self.assert_that_element_have_text(self.SECONDARY_HEADER, "Products")
        return self

    @allure.step("Проверка наличия списка товаров")
    def verify_inventory_list(self) -> "HomePage":
        self.assert_that_element_is_visible(self.INVENTORY_LIST)
        return self

    @allure.step("Проверка наличия футера")
    def verify_footer(self) -> "HomePage":
        self.assert_that_element_is_visible(self.FOOTER)
        return self

    @allure.step("Проверка значка количества добавленного товара в корзину")
    def verify_cart_badge_text(self, text: str) -> "HomePage":
        self.assert_that_element_have_text(self.SHOPPING_CART_BADGE, text)
        return self

    @allure.step("Проверка отсутствия кнопки Remove для товара {text}")
    def verify_remove_button_not_present(self, text: str) -> "HomePage":
        remove_locator = (
            By.XPATH,
            self._INVENTORY_ITEM_REMOVE_BUTTON[1].format(text=text)
        )
        elements = self.browser.find_elements(*remove_locator)
        assert not elements, f"Кнопка Remove для '{text}' все еще присутствует ({len(elements)} шт.)"
        return self

    @allure.step("Проверка отсутствия значка корзины (пустая корзина)")
    def verify_cart_badge_not_visible(self) -> "HomePage":
        elements = self.browser.find_elements(*self.SHOPPING_CART_BADGE)
        assert len(elements) == 0, "Badge корзины должен отсутствовать при пустой корзине"
        return self

    # ===== Методы для сортировки =====
    @allure.step("Выбор опции сортировки со значением {value}")
    def select_sort_option(self, value: str) -> "HomePage":
        select = Select(self.browser.find_element(*self.SORT_SELECT))
        select.select_by_value(value)  # az, za, lohi, hilo [web:79]
        return self

    @allure.step("Получение списка имен товаров на странице")
    def get_product_names(self) -> list[str]:
        elements = self.browser.find_elements(*self.ITEM_NAME)
        return [e.text for e in elements]

    @allure.step("Получение списка цен товаров на странице")
    def get_product_prices(self) -> list[float]:
        elements = self.browser.find_elements(*self.ITEM_PRICE)
        return [float(e.text.replace("$", "")) for e in elements]
