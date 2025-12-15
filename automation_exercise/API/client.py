import os
import json
import logging
import typing as t

import requests

from automation_exercise.utils.attach import attach_json, attach_text

logger = logging.getLogger("api")


class APIClient:
    def __init__(self, base_url: str | None = None, timeout: int = 20) -> None:
        self.base_url = (base_url or os.getenv("AUTOMATIONEXERCISE_API_URL", "https://www.automationexercise.com/api")).rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def request(self, method: str, endpoint: str, **kwargs) -> dict:
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

        # Allure attachments (request)
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

        # Пытаемся распарсить JSON независимо от content-type
        try:
            payload: t.Any = resp.json()
        except Exception:
            try:
                payload = json.loads(text)
            except Exception:
                payload = {"message": text}

        response_info = {
            "status_code": resp.status_code,
            "response": payload,
            "rawtext": text,
            "url": url,
            "method": method.upper(),
            "headers": dict(resp.headers),
        }

        # Логирование + Allure attachments (response)
        logger.info("Status: %s", resp.status_code)
        attach_text("response.status_code", str(resp.status_code))
        attach_json("response.headers", dict(resp.headers))
        attach_text("response.rawtext", text[:5000])  # ограничение на всякий случай
        attach_json("response.parsed", payload)

        return response_info
