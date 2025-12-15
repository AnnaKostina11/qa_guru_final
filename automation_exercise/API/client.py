import os
import logging
import typing as t

import requests

from automation_exercise.utils.attach import attach_json, attach_text


class APIClient:
    def __init__(self, base_url: str | None = None, timeout: int = 20) -> None:
        self.base_url = (base_url or os.getenv("AUTOMATIONEXERCISE_API_URL", "https://www.automationexercise.com/api")).rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.logger = logging.getLogger("APIClient")

    def request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)

        # Для аттачей/логов сохраним то, что уходит
        req_data = {
            "method": method.upper(),
            "url": url,
            "params": kwargs.get("params"),
            "data": kwargs.get("data"),
            "json": kwargs.get("json"),
            "headers": kwargs.get("headers"),
        }

        self.logger.info("API %s %s", method.upper(), url)
        if req_data["params"]:
            self.logger.info("Params: %s", req_data["params"])
        if req_data["data"]:
            self.logger.info("Data: %s", req_data["data"])
        if req_data["json"]:
            self.logger.info("Json: %s", req_data["json"])

        resp = self.session.request(method, url, **kwargs)

        content_type = resp.headers.get("content-type", "")
        if content_type.startswith("application/json"):
            payload: t.Any = resp.json()
        else:
            payload = {"message": resp.text}

        # Allure attachments
        attach_json("API Request", req_data)
        attach_text("API Response status", f"{resp.status_code}")
        attach_json("API Response", payload)

        self.logger.info("Status: %s", resp.status_code)

        return {
            "status_code": resp.status_code,
            "response": payload,
            "url": url,
            "method": method.upper(),
        }
