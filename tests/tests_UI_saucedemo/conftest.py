import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import browser
from dotenv import load_dotenv
from automation_exercise.utils import attach
import allure
import config

DEFAULT_BROWSER_VERSION = "128.0"
BASE_URL = os.getenv('BASE_URL', 'https://www.saucedemo.com')


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        action='store',
        default=DEFAULT_BROWSER_VERSION,
        help='Browser version for Selenoid (default: 128.0)'
    )
    parser.addoption(
        '--remote',
        action='store_true',
        default=False,
        help='Run tests in remote mode (Selenoid)'
    )


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='class', autouse=True)
def browser_setup(request):
    """Единая настройка браузера для всех тестов"""
    browser_version = "128.0"

    # ✅ Selene настройки
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 10.0

    # ✅ ✅ КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ: base_url как CALLABLE
    def open_base_url(path: str = "/") -> None:
        browser.open(BASE_URL.rstrip('/') + path)

    browser.config.base_url = open_base_url  # ← CALLABLE!

    # Определяем remote/local
    is_remote = bool(os.getenv('SELENOID_URL')) or request.config.getoption('remote')

    options = Options()

    if is_remote:
        selenoid_login = os.getenv("SELENOID_LOGIN")
        selenoid_pass = os.getenv("SELENOID_PASS")
        selenoid_url = os.getenv("SELENOID_URL")

        selenoid_capabilities = {
            "browserName": "chrome",
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True,
                "enableLog": True
            }
        }
        options.set_capability('selenoid:options', selenoid_capabilities['selenoid:options'])

        driver = webdriver.Remote(
            command_executor=f'https://{selenoid_login}:{selenoid_pass}@{selenoid_url}',
            options=options
        )
    else:
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

    browser.config.driver = driver
    browser.config.driver.maximize_window()

    yield browser

    # Allure attachments
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)
    browser.quit()


@pytest.fixture(scope="class")
def log_in_saucedemo():
    """Логин на saucedemo через Selene"""
    from pages.authorization_page import AuthorizationPage
    from pages.home_page import HomePage

    auth = AuthorizationPage(browser)
    auth.open_authorization_page()  # ✅ Теперь работает!
    auth.fill_username(config.SAUCEDEMO_LOGIN)
    auth.fill_password(config.SAUCEDEMO_PASSWORD)
    auth.submit()

    HomePage(browser).verify_url()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        item.status = "failed"
    else:
        item.status = "passed"
