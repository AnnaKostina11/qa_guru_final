import json
import logging
import os
import typing as t

import requests

from automation_exercise.utils.attach import attach_json, attach_text

logger = logging.getLogger("api")


class APIClient:

    def __init__(self, base_url: str | None = None, timeout: int = 20) -> None:
        self.base_url = (
                base_url
                or os.getenv("AUTOMATIONEXERCISE_API_URL", "https://www.automationexercise.com/api")
        ).rstrip("/")

        # Таймаут по умолчанию на каждый запрос
        self.timeout = timeout

        self.session = requests.Session()

    def request(self, method: str, endpoint: str, **kwargs) -> dict:
        # Собираем конечный URL: base_url + endpoint.
        url = f"{self.base_url}{endpoint}"

        # Проставляем timeout, если вызывающий его не передал.
        kwargs.setdefault("timeout", self.timeout)

        # Дублируем базовую информацию в лог
        logger.info("HTTP %s %s", method.upper(), url)
        if "params" in kwargs:
            logger.info("Params: %s", kwargs["params"])
        if "data" in kwargs:
            logger.info("Data: %s", kwargs["data"])
        if "json" in kwargs:
            logger.info("JSON: %s", kwargs["json"])

        # Прикладываем request в Allure
        attach_text("request.method", method.upper())
        attach_text("request.url", url)

        if "params" in kwargs:
            attach_json("request.params", kwargs["params"])
        if "data" in kwargs:
            attach_text("request.data", str(kwargs["data"]))
        if "json" in kwargs:
            attach_json("request.json", kwargs["json"])

        # Выполняем HTTP-запрос.
        resp = self.session.request(method, url, **kwargs)
        text = resp.text

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

        # Response логируем и прикладываем в Allure.
        logger.info("Status: %s", resp.status_code)
        attach_text("response.status_code", str(resp.status_code))
        attach_json("response.headers", dict(resp.headers))
        attach_text("response.rawtext", text[:5000])
        attach_json("response.parsed", payload)

        return response_info
