import logging
import typing as t

import requests
from selene.support.shared import browser

from automation_exercise.utils.attach import attach_json, attach_text

logger = logging.getLogger("api")


class APIClient:
    def __init__(self, base_url: str | None = None, timeout: int = 20) -> None:
        self.base_url = (base_url or browser.config.base_url or "").rstrip("/")
        if not self.base_url:
            raise RuntimeError("API base_url is empty. Set browser.config.base_url in conftest.py")

        self.timeout = timeout
        self.session = requests.Session()

    def request(self, method: str, endpoint: str, **kwargs) -> dict:
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)

        # Логирование в консоль
        logger.info("HTTP %s %s", method.upper(), url)

        if "params" in kwargs:
            logger.info("Params: %s", kwargs["params"])
        if "data" in kwargs:
            logger.info("Data: %s", kwargs["data"])
        if "json" in kwargs:
            logger.info("JSON: %s", kwargs["json"])

        # Allure request
        attach_text("request.method", method.upper())
        attach_text("request.url", url)
        if "params" in kwargs:
            attach_json("request.params", kwargs["params"])
        if "data" in kwargs:
            attach_text("request.data", str(kwargs["data"]))
        if "json" in kwargs:
            attach_json("request.json", kwargs["json"])

        resp = self.session.request(method, url, **kwargs)
        text = resp.text

        try:
            payload: t.Any = resp.json()
        except Exception:
            payload = {"message": text}

        # Логирование в консоль
        logger.info("Status: %s %s", resp.status_code, url)

        # Allure response
        attach_text("response.status_code", str(resp.status_code))
        attach_json("response.headers", dict(resp.headers))
        attach_text("response.rawtext", text[:5000])
        attach_json("response.parsed", payload)

        return {
            "status_code": resp.status_code,
            "response": payload,
            "rawtext": text,
            "url": url,
            "method": method.upper(),
            "headers": dict(resp.headers),
        }
