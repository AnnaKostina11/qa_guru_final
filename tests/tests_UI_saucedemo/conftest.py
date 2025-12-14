import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import browser
from selene.support.shared import config
from dotenv import load_dotenv
from automation_exercise.utils import attach

DEFAULT_BROWSER_VERSION = "128.0"
BASE_URL = os.getenv('SAUCEDEMO_URL')


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default=DEFAULT_BROWSER_VERSION
    )


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='class', autouse=True)  # ✅ scope='class' для всех UI тестов
def browser_setup(request):
    """Единая настройка Selenoid браузера для класса тестов"""
    browser_version = request.config.getoption('browser_version') or DEFAULT_BROWSER_VERSION

    # ✅ Selene config ДО создания драйвера
    config.timeout = 6.0
    config.window_width = 1920
    config.window_height = 1080
    config.base_url = BASE_URL

    options = Options()

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

    # ✅ Правильная настройка capabilities для Remote
    login = os.getenv('SELENOID_LOGIN')
    password = os.getenv('SELENOID_PASS')
    url = os.getenv('SELENOID_URL')

    options.set_capability('browserName', 'chrome')
    options.set_capability('browserVersion', browser_version)
    options.set_capability('selenoid:options', selenoid_capabilities['selenoid:options'])

    driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@{url}/wd/hub",  # ✅ /wd/hub
        options=options
    )

    browser.config.driver = driver
    browser.config.driver.maximize_window()

    yield browser

    # ✅ Cleanup
    try:
        attach.add_screenshot(browser)
        attach.add_logs(browser)
        attach.add_html(browser)
        attach.add_video(browser)
        browser.quit()
    except:
        pass


@pytest.fixture(scope="class")  # ✅ Теперь совместим с browser_setup
def log_in_saucedemo(browser_setup):
    """Успешный логин на saucedemo"""
    from pages.authorization_page import AuthorizationPage
    auth = AuthorizationPage(browser)
    auth.open_authorization_page()
    auth.fill_username(os.getenv('SAUCEDEMO_LOGIN'))
    auth.fill_password(os.getenv('SAUCEDEMO_PASSWORD'))
    auth.submit()


@pytest.fixture(scope="class")  # ✅ Теперь совместим с browser_setup
def log_in_saucedemo_fail(browser_setup):
    """Неуспешный логин на saucedemo"""
    from pages.authorization_page import AuthorizationPage
    auth = AuthorizationPage(browser)
    auth.open_authorization_page()
    auth.fill_username(os.getenv('SAUCEDEMO_LOGIN_FAIL'))
    auth.fill_password(os.getenv('SAUCEDEMO_PASSWORD'))
    auth.submit()
