import os

import allure
import pytest
from allure_commons.types import AttachmentType
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.authorization_page import AuthorizationPage
from pages.inventory_page import InventoryPage


# Один раз за сессию подгружаем переменные окружения из .env
@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


# Строим ссылку на видео Селеноид
def _video_url(session_id: str) -> str:
    base = os.getenv("SELENOID_URL")
    base = base.replace("/wd/hub", "")
    return f"https://{base}/video/{session_id}.mp4"


# Выкладываем результаты в Аллюр после выполнения теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    # Скриншот браузера на момент завершения теста
    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name="Screenshot",
        attachment_type=AttachmentType.PNG,
    )

    # HTML-код страницы для анализа состояния UI
    allure.attach(
        browser.driver.page_source,
        name="PageSource",
        attachment_type=AttachmentType.HTML,
    )

    # Логи браузера
    try:
        logs = browser.driver.get_log("browser")
        allure.attach(
            "\n".join(str(x) for x in logs),
            name="Browser console logs",
            attachment_type=AttachmentType.TEXT,
        )
    except AttributeError:
        pass

    # Ссылка на видео из Селеноид
    allure.attach(
        _video_url(browser.driver.session_id),
        name="Video URL",
        attachment_type=AttachmentType.URI_LIST,
    )


# Логин в приложение и возврат страницы с товарами как стартового состояния
@pytest.fixture
def logged_in(browser_setup):
    (
        AuthorizationPage()
        .open_authorization_page()
        .fill_username(os.getenv("SAUCEDEMO_LOGIN"))
        .fill_password(os.getenv("SAUCEDEMO_PASSWORD"))
        .submit()
    )
    return InventoryPage().should_be_opened()


# Конфигурируем и поднимаем драйвер перед каждым тестом
@pytest.fixture(scope="function", autouse=True)
def browser_setup():
    # Определение режима запуска: локально или через Selenoid
    run_mode = os.getenv("RUN_MODE")
    use_remote = run_mode in {"remote"}

    # Базовые настройки Селен
    browser.config.timeout = float(os.getenv("UI_TIMEOUT", "6.0"))
    browser.config.base_url = os.getenv(
        "SAUCEDEMO_URL", "https://www.saucedemo.com"
    )
    width = int(os.getenv("UI_WIDTH", "1920"))
    height = int(os.getenv("UI_HEIGHT", "1080"))

    # Конфигурация браузера
    options = Options()
    options.set_capability("browserName", "chrome")

    browser_version = os.getenv("BROWSER_VERSION")
    options.set_capability("browserVersion", browser_version)

    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    options.set_capability("acceptInsecureCerts", True)
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )

    # Отключение всплывающих уведомлений и инфобара
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")

    if use_remote:
        # Настройка подключения к Селеноид
        url = os.getenv("SELENOID_URL")
        login = os.getenv("SELENOID_LOGIN")
        password = os.getenv("SELENOID_PASS")
        auth_url = f"https://{login}:{password}@{url}"

        # Дополнительные опции Селеноид для удаленного подключения, записи видео и включения лога
        options.set_capability(
            "selenoid:options",
            {
                "enableVNC": True,
                "enableVideo": True,
                "enableLog": True,
            },
        )

        # Создание удаленного WebDriver в Селеноид
        driver = webdriver.Remote(command_executor=auth_url, options=options)
    else:
        # Локальный запуск Chrome-драйвера
        driver = webdriver.Chrome(options=options)

    # Привязка драйвера к Селен и установка размера окна
    browser.config.driver = driver
    browser.driver.set_window_size(width, height)

    # Передача сконфигурированного браузера в тест и закрытие после
    yield browser

    browser.quit()
