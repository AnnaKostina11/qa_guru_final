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


# ✅ ИСПРАВЛЕННЫЙ BROWSER FIXTURE
@pytest.fixture(scope='class', autouse=True)
def browser_setup(request):
    """Единая настройка браузера для всех тестов"""
    # ✅ Теперь работает - опция зарегистрирована выше
    browser_version = request.config.getoption('--browser_version') or DEFAULT_BROWSER_VERSION

    # Настройки Selene
    browser.config.base_url = BASE_URL
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 10.0

    # ✅ Исправлено: проверка через os.getenv()
    is_remote = bool(os.getenv('SELENOID_URL')) or request.config.getoption('remote')

    options = Options()

    if is_remote:
        # ✅ Безопасные значения по умолчанию
        login = os.getenv('SELENOID_LOGIN', 'admin')
        password = os.getenv('SELENOID_PASSWORD', 'admin')
        url = os.getenv('SELENOID_URL', 'selenoid.default.svc.cluster.local')

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
            command_executor=f'https://{login}:{password}@{url}/wd/hub',
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
