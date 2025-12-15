import os
import typing as t

import requests


class APIClient:
    def __init__(self, base_url: str | None = None, timeout: int = 20) -> None:
        self.base_url = (base_url or os.getenv("AUTOMATIONEXERCISE_API_URL", "https://www.automationexercise.com/api")).rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)

        resp = self.session.request(method, url, **kwargs)

        content_type = resp.headers.get("content-type", "")
        if content_type.startswith("application/json"):
            payload: t.Any = resp.json()
        else:
            payload = {"message": resp.text}

        return {
            "status_code": resp.status_code,
            "response": payload,
            "url": url,
            "method": method.upper(),
        }
