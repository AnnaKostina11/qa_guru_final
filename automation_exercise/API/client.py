import os
import json
import logging
import typing as t

import requests

from automation_exercise.utils.attach import attach_json, attach_text

logger = logging.getLogger("api")


class APIClient:
    # Низкоуровневый HTTP-клиент:
    # - строит URL (base_url + endpoint)
    # - делает request через requests.Session (переиспользование соединений)
    # - логирует и прикладывает request/response в Allure
    # - пытается распарсить ответ как JSON, иначе хранит raw text

    def __init__(self, base_url: str | None = None, timeout: int = 20) -> None:
        # base_url можно переопределить через env или параметром (удобно для разных стендов).
        self.base_url = (
            base_url
            or os.getenv("AUTOMATIONEXERCISE_API_URL", "https://www.automationexercise.com/api")
        ).rstrip("/")

        # Таймаут по умолчанию на каждый запрос (секунды).
        self.timeout = timeout

        # Session даёт keep-alive и общие настройки для всех запросов.
        self.session = requests.Session()

    def request(self, method: str, endpoint: str, **kwargs) -> dict:
        # Собираем конечный URL: base_url + endpoint.
        url = f"{self.base_url}{endpoint}"

        # Проставляем timeout, если вызывающий его не передал.
        kwargs.setdefault("timeout", self.timeout)

        # Дублируем базовую информацию в лог (полезно при отладке CI).
        logger.info("HTTP %s %s", method.upper(), url)
        if "params" in kwargs:
            logger.info("Params: %s", kwargs["params"])
        if "data" in kwargs:
            logger.info("Data: %s", kwargs["data"])
        if "json" in kwargs:
            logger.info("JSON: %s", kwargs["json"])

        # Прикладываем request в Allure, чтобы в отчёте было видно что именно отправлялось.
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

        # Пытаемся получить JSON нормальным путём (requests.json()).
        # Если не получилось — пробуем руками json.loads(text).
        # Если и это не получилось — сохраняем как {"message": raw_text}.
        try:
            payload: t.Any = resp.json()
        except Exception:
            try:
                payload = json.loads(text)
            except Exception:
                payload = {"message": text}

        # Единый формат, который ожидают тесты и BaseTestRequests.check_response().
        response_info = {
            "status_code": resp.status_code,
            "response": payload,
            "rawtext": text,
            "url": url,
            "method": method.upper(),
            "headers": dict(resp.headers),
        }

        # Response тоже логируем и прикладываем в Allure.
        logger.info("Status: %s", resp.status_code)
        attach_text("response.status_code", str(resp.status_code))
        attach_json("response.headers", dict(resp.headers))
        attach_text("response.rawtext", text[:5000])
        attach_json("response.parsed", payload)

        return response_info
