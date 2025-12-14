import os
import pytest
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selene import browser
from selene.support.shared import config

# лучше брать после load_dotenv, поэтому дефолт только тут:
DEFAULT_BROWSER_VERSION = "128.0"


def pytest_addoption(parser):
    parser.addoption("--browser_version", default=DEFAULT_BROWSER_VERSION)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def browser_setup(request):
    browser_version = request.config.getoption("browser_version") or DEFAULT_BROWSER_VERSION

    # Selene config
    config.timeout = 6.0
    config.window_width = 1920
    config.window_height = 1080
    config.base_url = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com")

    options = Options()
    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", browser_version)
    options.set_capability(
        "selenoid:options",
        {"enableVNC": True, "enableVideo": True, "enableLog": True},
    )
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    options.set_capability("acceptInsecureCerts", True)

    login = os.getenv("SELENOID_LOGIN")
    password = os.getenv("SELENOID_PASS")
    url = os.getenv("SELENOID_URL")  # например: selenoid.company.local:4444/wd/hub

    # важно: в SELENOID_URL должен быть корректный endpoint, обычно /wd/hub
    command_executor = f"https://{login}:{password}@{url}"

    driver = webdriver.Remote(command_executor=command_executor, options=options)
    browser.config.driver = driver

    yield browser

    # cleanup
    browser.quit()
