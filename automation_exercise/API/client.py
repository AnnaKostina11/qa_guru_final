import os
import json
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

        text = resp.text
        payload: t.Any

        # 1) Пытаемся распарсить как JSON независимо от content-type
        try:
            payload = resp.json()
        except Exception:
            # 2) Если resp.json() не смог, пробуем руками распарсить текст
            try:
                payload = json.loads(text)
            except Exception:
                payload = {"message": text}

        return {
            "status_code": resp.status_code,
            "response": payload,
            "rawtext": text,
            "url": url,
            "method": method.upper(),
        }
