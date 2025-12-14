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


# ✅ РЕГИСТРАЦИЯ ОПЦИЙ (ОБЯЗАТЕЛЬНО!)
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



import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import Browser, Config

from automation_exercise.utils import attach
from dotenv import load_dotenv
import os

@pytest.fixture(scope='function')
def setup_browser(request):
    load_dotenv()
    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")

    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "128.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}",
        options=options
    )

    browser = Browser(Config(driver=driver))

    browser.driver.set_window_size(1920, 2000)

    yield browser

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()


# ✅ LOGIN FIXTURE (без изменений)
@pytest.fixture(scope="class")
def log_in_saucedemo():
    """Логин на saucedemo через Selene"""
    from pages.authorization_page import AuthorizationPage
    from pages.home_page import HomePage

    auth = AuthorizationPage(browser)
    auth.open_authorization_page()
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
