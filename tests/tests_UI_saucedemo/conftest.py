import os

import pytest
from selene import browser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import Browser, Config
from dotenv import load_dotenv
from automation_exercise.utils import attach

DEFAULT_BROWSER_VERSION = "128.0"
BASE_URL = os.getenv('SAUCEDEMO_URL')

def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='128.0'
    )

@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture(scope="class")
def log_in_saucedemo(browser_setup):
    from pages.authorization_page import AuthorizationPage

    auth = AuthorizationPage(browser)
    auth.open_authorization_page()
    auth.fill_username(os.getenv('SAUCEDEMO_LOGIN'))
    auth.fill_password(os.getenv('SAUCEDEMO_PASSWORD'))
    auth.submit()

@pytest.fixture(scope="class")
def log_in_saucedemo_fail(browser_setup):
    from pages.authorization_page import AuthorizationPage

    auth = AuthorizationPage(browser)
    auth.open_authorization_page()
    auth.fill_username(os.getenv('SAUCEDEMO_LOGIN_FAILED'))
    auth.fill_password(os.getenv('SAUCEDEMO_PASSWORD'))
    auth.submit()


@pytest.fixture(scope='function', autouse=True)
def browser_setup(request):
    browser_version = DEFAULT_BROWSER_VERSION
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
    login = os.getenv('SELENOID_LOGIN')
    password = os.getenv('SELENOID_PASS')
    url = os.getenv('SELENOID_URL')
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