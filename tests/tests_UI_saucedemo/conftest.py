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
BASE_URL = os.getenv('OFF_BASE_URL', 'https://world.openfoodfacts.org')

def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='128.0'
    )

@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    # options = Options()
    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
    options = webdriver.ChromeOptions()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True,
            "enableLog": True
        },
        "goog:loggingPrefs": {"browser": "ALL"}
    }
    login = os.getenv('SAUCEDEMO_LOGIN')
    password = os.getenv('SAUCEDEMO_PASSWORD')
    url = os.getenv('SAUCEDEMO_URL')
    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@{url}",
        options=options
    )
    browser.config.driver = driver
    browser.config.driver.maximize_window()
    browser.config.base_url = BASE_URL
    browser.config.timeout = 6


    yield browser

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()


@allure.title('Инициализация браузера.')
@pytest.fixture(scope='function', autouse=True)
def manage_browser(request):
    # Настройка конфигурации Selene
    browser.config.base_url = os.getenv('BASE_URL', 'https://www.saucedemo.com')
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 10.0

    is_remote = request.config.getoption('remote')

    if is_remote:
        selenoid_login = os.getenv('SELENOID_LOGIN')
        selenoid_pass = os.getenv('SELENOID_PASS')
        selenoid_url = os.getenv('SELENOID_URL', 'selenoid.default.svc.cluster.local')

        selenoid_capabilities = {
            'browserName': 'chrome',
            'browserVersion': '128.0',
            'selenoid:options': {
                'enableVideo': True,
                'enableVNC': True,
                'screenResolution': '1920x1080x24'
            }
        }

        options = Options()
        options.set_capability('selenoid:options', selenoid_capabilities['selenoid:options'])

        # Selene автоматически подхватит драйвер
        browser.config.driver = webdriver.Remote(
            command_executor=f'https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub',
            options=options
        )
    else:
        # Локальный Chrome
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        browser.config.driver = webdriver.Chrome(options=options)

    yield  # Selene управляет браузером

    # Финализация с Allure
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        item.status = "failed"
    else:
        item.status = "passed"


@pytest.fixture(scope="class")
def log_in_saucedemo(browser):
    """Логин на saucedemo через Selene"""
    from pages.authorization_page import AuthorizationPage
    from pages.home_page import HomePage

    auth = AuthorizationPage(browser)
    auth.open_authorization_page()
    auth.fill_username(config.SAUCEDEMO_LOGIN)
    auth.fill_password(config.SAUCEDEMO_PASSWORD)
    auth.submit()

    HomePage(browser).verify_url()
