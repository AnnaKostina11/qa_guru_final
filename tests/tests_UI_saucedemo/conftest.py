import os
from pathlib import Path

import allure
import pytest
import requests
from allure_commons.types import AttachmentType
from dotenv import load_dotenv
from selene import browser
from selene.support.shared import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DEFAULT_BROWSER_VERSION = "128.0"


def pytest_addoption(parser):
    parser.addoption("--browser_version", default=DEFAULT_BROWSER_VERSION)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


def _attach_screenshot():
    try:
        allure.attach(
            browser.driver.get_screenshot_as_png(),
            name="Screenshot",
            attachment_type=AttachmentType.PNG,
        )
    except Exception:
        pass


def _attach_page_source():
    try:
        allure.attach(
            browser.driver.page_source,
            name="PageSource",
            attachment_type=AttachmentType.HTML,
        )
    except Exception:
        pass


def _attach_browser_logs():
    try:
        logs = browser.driver.get_log("browser")
        text = "\n".join(str(x) for x in logs)
        allure.attach(text, name="Browser console logs", attachment_type=AttachmentType.TEXT)
    except Exception:
        pass


def _build_video_url(session_id: str) -> str | None:

    selenoid_ui = (os.getenv("SELENOID_UI") or "").rstrip("/")
    if selenoid_ui:
        return f"{selenoid_ui}/video/{session_id}.mp4"

    raw = (os.getenv("SELENOID_URL") or "").strip()
    if not raw:
        return None

    raw = raw.replace("/wd/hub", "").rstrip("/")
    if not raw.startswith("http://") and not raw.startswith("https://"):
        raw = "https://" + raw

    return f"{raw}/video/{session_id}.mp4"


def _attach_video():
    try:
        session_id = browser.driver.session_id
    except Exception:
        return

    video_url = _build_video_url(session_id)
    if not video_url:
        return

    try:
        allure.attach(video_url, name="Video URL", attachment_type=AttachmentType.URI_LIST)
    except Exception:
        pass

    try:
        target = Path("artifacts") / f"{session_id}.mp4"
        target.parent.mkdir(parents=True, exist_ok=True)

        r = requests.get(video_url, timeout=40)
        r.raise_for_status()
        target.write_bytes(r.content)

        allure.attach.file(str(target), name="Video", attachment_type=AttachmentType.MP4)
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    _attach_screenshot()
    _attach_page_source()
    _attach_browser_logs()
    _attach_video()


@pytest.fixture(scope="function", autouse=True)
def browser_setup(request):
    browser_version = request.config.getoption("browser_version") or DEFAULT_BROWSER_VERSION

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
    url = os.getenv("SELENOID_URL")

    command_executor = f"https://{login}:{password}@{url}"

    driver = webdriver.Remote(command_executor=command_executor, options=options)
    browser.config.driver = driver

    yield browser

    browser.quit()
