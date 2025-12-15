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

        req_data = {
            "method": method.upper(),
            "url": url,
            "params": kwargs.get("params"),
            "data": kwargs.get("data"),
            "json": kwargs.get("json"),
            "headers": kwargs.get("headers"),
        }

        self.logger.info("API %s %s", method.upper(), url)

        resp = self.session.request(method, url, **kwargs)

        content_type = resp.headers.get("content-type", "")
        text = resp.text

        payload: t.Any
        if "application/json" in content_type.lower():
            try:
                payload = resp.json()
            except Exception:
                payload = {"message": text}
        else:
            payload = {"message": text}

        # Allure attachments (не ломают тесты, даже если что-то пойдёт не так)
        try:
            attach_json("API Request", req_data)
            attach_text("API Response status", str(resp.status_code))
            attach_text("API Response content-type", content_type)
            attach_text("API Response raw text", text[:5000])
            if isinstance(payload, (dict, list)):
                attach_json("API Response parsed", payload)
        except Exception:
            pass

        return {
            "status_code": resp.status_code,
            "response": payload,   # <-- гарантированно dict/list (или {"message": text})
            "raw_text": text,
            "url": url,
            "method": method.upper(),
        }
