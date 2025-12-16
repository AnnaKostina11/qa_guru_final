import os
from pathlib import Path

import allure
import pytest
import requests
from allure_commons.types import AttachmentType
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.client_config import ClientConfig


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


def _create_chrome_options(browser_version: str) -> Options:
    options = Options()
    options.set_capability("browserName", "chrome")

    if browser_version:
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

    return options


def _make_remote_driver(options: Options) -> webdriver.Remote:
    url = (os.getenv("SELENOID_URL") or "").strip()
    if not url:
        raise RuntimeError("SELENOID_URL is required for RUN_MODE=remote")

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    client_config = ClientConfig(remote_server_addr=url)

    login = (os.getenv("SELENOID_LOGIN") or "").strip()
    password = (os.getenv("SELENOID_PASS") or "").strip()
    if login and password:
        client_config.username = login
        client_config.password = password

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.set_capability(
        "selenoid:options",
        {"enableVNC": True, "enableVideo": True, "enableLog": True},
    )

    return webdriver.Remote(options=options, client_config=client_config)


def _build_video_url(session_id: str) -> str | None:
    selenoid_ui = (os.getenv("SELENOID_UI") or "").rstrip("/")
    if selenoid_ui:
        return f"{selenoid_ui}/video/{session_id}.mp4"

    raw = (os.getenv("SELENOID_URL") or "").strip()
    if not raw:
        return None

    raw = raw.replace("/wd/hub", "").rstrip("/")
    if not raw.startswith(("http://", "https://")):
        raw = "http://" + raw

    return f"{raw}/video/{session_id}.mp4"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    # attachments (best-effort)
    try:
        allure.attach(
            browser.driver.get_screenshot_as_png(),
            name="Screenshot",
            attachment_type=AttachmentType.PNG,
        )
    except Exception:
        pass

    try:
        allure.attach(
            browser.driver.page_source,
            name="PageSource",
            attachment_type=AttachmentType.HTML,
        )
    except Exception:
        pass

    try:
        logs = browser.driver.get_log("browser")
        allure.attach(
            "\n".join(str(x) for x in logs),
            name="Browser console logs",
            attachment_type=AttachmentType.TEXT,
        )
    except Exception:
        pass

    # video (only if available)
    try:
        session_id = browser.driver.session_id
        video_url = _build_video_url(session_id)
        if video_url:
            allure.attach(video_url, name="Video URL", attachment_type=AttachmentType.URI_LIST)

            target = Path("artifacts") / f"{session_id}.mp4"
            target.parent.mkdir(parents=True, exist_ok=True)

            r = requests.get(video_url, timeout=40)
            r.raise_for_status()
            target.write_bytes(r.content)

            allure.attach.file(str(target), name="Video", attachment_type=AttachmentType.MP4)
    except Exception:
        pass


@pytest.fixture(scope="function", autouse=True)
def browser_setup():
    run_mode = (os.getenv("RUN_MODE") or "local").strip().lower()
    use_remote = run_mode in {"remote", "selenoid"}

    browser_version = (os.getenv("BROWSER_VERSION") or "").strip()
    browser.config.timeout = float(os.getenv("UI_TIMEOUT", "6.0"))
    browser.config.base_url = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com").rstrip("/")

    width = int(os.getenv("UI_WIDTH", "1920"))
    height = int(os.getenv("UI_HEIGHT", "1080"))

    options = _create_chrome_options(browser_version)

    driver = _make_remote_driver(options) if use_remote else webdriver.Chrome(options=options)

    browser.config.driver = driver
    browser.driver.set_window_size(width, height)

    yield browser

    browser.quit()
