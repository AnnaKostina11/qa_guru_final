import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    APP_LOGO = By.CSS_SELECTOR, ".app_logo"
    SHOPPING_CART_LINK = By.CSS_SELECTOR, "[data-test=shopping-cart-link]"
    SECONDARY_HEADER = By.CSS_SELECTOR, "[data-test=secondary-header]"
    CART_LIST = By.CSS_SELECTOR, "[data-test=cart-list]"
    CONTINUE_SHOPPING_BUTTON = By.CSS_SELECTOR, "#continue-shopping"
    CHECKOUT_BUTTON = By.CSS_SELECTOR, "#checkout"
    FOOTER = By.CSS_SELECTOR, "[data-test=footer]"
    INVENTORY_ITEM = By.CSS_SELECTOR, "[data-test=inventory-item]"
    FIRST_NAME_FIELD = By.CSS_SELECTOR, "[data-test=firstName]"
    LAST_NAME_FIELD = By.CSS_SELECTOR, "[data-test=lastName]"
    POSTAL_CODE_FIELD = By.CSS_SELECTOR, "[data-test=postalCode]"
    CONTINUE_BUTTON = By.CSS_SELECTOR, "#continue"
    FINISH_BUTTON = By.CSS_SELECTOR, "#finish"
    COMPLETE_HEADER = By.CSS_SELECTOR, "[data-test=complete-header]"

    # ACTIONS
    @allure.step("Ввод имени {value}")
    def fill_first_name(self, value: str) -> None:
        self.type_text_into_element(self.FIRST_NAME_FIELD, value)

    @allure.step("Ввод фамилии {value}")
    def fill_last_name(self, value: str) -> None:
        self.type_text_into_element(self.LAST_NAME_FIELD, value)

    @allure.step("Ввод кода {value}")
    def fill_postal_code(self, value: str) -> None:
        self.type_text_into_element(self.POSTAL_CODE_FIELD, value)

    @allure.step("Нажатие кнопки выбора")
    def click_checkout_button(self) -> None:
        self.click_on_element(self.CHECKOUT_BUTTON)

    @allure.step("Нажатие кнопки продолжения")
    def click_continue_button(self) -> None:
        self.click_on_element(self.CONTINUE_BUTTON)

    @allure.step("Нажатие кнопки завершения покупки")
    def click_finish_button(self) -> None:
        self.click_on_element(self.FINISH_BUTTON)

    # VERIFICATION
    @allure.step("Проверка URL страницы")
    def verify_page_url(self) -> None:
        self.assert_that_url_contains("cart")

    @allure.step("Проверка title страницы")
    def verify_page_title(self) -> None:
        self.assert_that_page_have_title("Swag Labs")

    @allure.step("Проверка логотипа страницы")
    def verify_app_logo(self) -> None:
        self.assert_that_element_have_text(self.APP_LOGO, "Swag Labs")

    @allure.step("Проверка наличия ссылки на корзину")
    def verify_shopping_cart_link(self) -> None:
        self.assert_that_element_is_visible(self.SHOPPING_CART_LINK)

    @allure.step("Проверка второго заголовка страницы")
    def verify_secondary_header(self) -> None:
        self.assert_that_element_have_text(self.SECONDARY_HEADER, "Your Cart")

    @allure.step("Проверка наличия списка покупок")
    def verify_cart_list(self) -> None:
        self.assert_that_element_is_visible(self.CART_LIST)

    @allure.step("Проверка наличия кнопки возврата к списку покупок")
    def verify_continue_shopping_button(self) -> None:
        self.assert_that_element_is_visible(self.CONTINUE_SHOPPING_BUTTON)

    @allure.step("Проверка наличия кнопки выбора товаров и продолжения покупок")
    def verify_checkout_button(self) -> None:
        self.assert_that_element_is_visible(self.CHECKOUT_BUTTON)

    @allure.step("Проверка наличия футера страницы")
    def verify_footer(self) -> None:
        self.assert_that_element_is_visible(self.FOOTER)

    @allure.step("Проверка, что количество товаров в корзине равно {count}")
    def verify_count_of_inventory_items(self, count: int) -> None:
        self.assert_that_count_of_elements_equal(self.INVENTORY_ITEM, count)

    @allure.step("Проверка сообщения об успешной покупке")
    def verify_complete_header(self) -> None:
        self.assert_that_element_have_text(
            self.COMPLETE_HEADER,
            "Thank you for your order!",
        )