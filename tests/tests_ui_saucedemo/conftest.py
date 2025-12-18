import os

import allure
import pytest
from allure_commons.types import AttachmentType
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.client_config import ClientConfig
from pages.authorization_page import AuthorizationPage
from pages.inventory_page import InventoryPage

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


def _video_url(session_id: str) -> str:
    base = os.getenv("SELENOID_URL")
    base = base.replace("/wd/hub", "")
    return f"https://{base}/video/{session_id}.mp4"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name="Screenshot",
        attachment_type=AttachmentType.PNG,
    )
    allure.attach(
        browser.driver.page_source,
        name="PageSource",
        attachment_type=AttachmentType.HTML,
    )

    try:
        logs = browser.driver.get_log("browser")
        allure.attach(
            "\n".join(str(x) for x in logs),
            name="Browser console logs",
            attachment_type=AttachmentType.TEXT,
        )
    except AttributeError:
        print("Browser logs unavailable")

    allure.attach(
        _video_url(browser.driver.session_id),
        name="Video URL",
        attachment_type=AttachmentType.URI_LIST,
    )

@pytest.fixture
def logged_in(browser_setup):
    AuthorizationPage() \
        .open_authorization_page() \
        .fill_username(os.getenv("SAUCEDEMO_LOGIN")) \
        .fill_password(os.getenv("SAUCEDEMO_PASSWORD")) \
        .submit()
    return InventoryPage().should_be_opened()

@pytest.fixture(scope="function", autouse=True)
def browser_setup():
    run_mode = os.getenv("RUN_MODE")
    use_remote = run_mode in {"remote"}
    browser.config.timeout = float(os.getenv("UI_TIMEOUT", "6.0"))
    browser.config.base_url = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com")
    width = int(os.getenv("UI_WIDTH", "1920"))
    height = int(os.getenv("UI_HEIGHT", "1080"))

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
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")

    if use_remote:
        url = os.getenv("SELENOID_URL")

        login = os.getenv("SELENOID_LOGIN")
        password = os.getenv("SELENOID_PASS")
        auth_url = f"https://{login}:{password}@{url}"
        options.set_capability("selenoid:options", {
            "enableVNC": True,
            "enableVideo": True,
            "enableLog": True
        })
        driver = webdriver.Remote(command_executor=auth_url, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    browser.config.driver = driver
    browser.driver.set_window_size(width, height)

    yield browser

    browser.quit()
