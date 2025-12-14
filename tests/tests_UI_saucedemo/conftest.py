import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import browser  # ✅ Только browser
from selene.support.shared import config  # ✅ Импорт config
from dotenv import load_dotenv
from automation_exercise.utils import attach
import allure

DEFAULT_BROWSER_VERSION = "128.0"
selenoid_login = os.getenv("SELENOID_LOGIN")
selenoid_pass = os.getenv("SELENOID_PASS")
selenoid_url = os.getenv("SELENOID_URL")
s_user = os.getenv("SAUCEDEMO_LOGIN")
s_password = os.getenv("SAUCEDEMO_PASSWORD")
s_url = os.getenv("SAUCEDEMO_URL")


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


@pytest.fixture(scope='class', autouse=True)  # ✅ ИЗМЕНЕНО с function на class
def browser_setup(request):
    """Единая настройка браузера для всех тестов класса"""
    browser_version = request.config.getoption('browser_version')  # ✅ Без --
    browser_version = browser_version if browser_version else DEFAULT_BROWSER_VERSION

    # ✅ Selene настройки ПЕРЕД драйвером
    config.timeout = 6.0
    config.window_width = 1920
    config.window_height = 1080

    options = webdriver.ChromeOptions()

    # ✅ Проверяем наличие Selenoid переменных
    if all([selenoid_login, selenoid_pass, selenoid_url]):
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
        options.set_capability('selenoid:options', selenoid_capabilities['selenoid:options'])
        options.set_capability('browserName', 'chrome')
        options.set_capability('browserVersion', browser_version)

        driver = webdriver.Remote(
            command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}",  # ✅ /wd/hub
            options=options
        )
    else:
        # ✅ Локальный Chrome
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        driver = webdriver.Chrome(options=options)

    browser.config.driver = driver
    browser.config.driver.maximize_window()

    yield browser

    # ✅ Allure attachments в try-except
    try:
        attach.add_screenshot(browser)
        attach.add_logs(browser)
        attach.add_html(browser)
        attach.add_video(browser)
    except Exception:
        pass

    browser.quit()


@pytest.fixture(scope="class")
def log_in_saucedemo(browser_setup):
    """Логин на saucedemo через Selene"""
    from pages.authorization_page import AuthorizationPage

    auth = AuthorizationPage(browser)
    auth.open_authorization_page()
    auth.fill_username(s_user)
    auth.fill_password(s_password)
    auth.submit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        if rep.failed:
            item.status = "failed"
        else:
            item.status = "passed"
