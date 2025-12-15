import json

import allure
from allure_commons.types import AttachmentType


def attach_json(name: str, data) -> None:
    # Allure attach для структурированных данных (request/response, params и т.п.)
    # Делаем pretty-print, чтобы удобнее читать в отчёте.
    allure.attach(
        json.dumps(data, ensure_ascii=False, indent=2),
        name=name,
        attachment_type=AttachmentType.JSON,
    )


def attach_text(name: str, text: str) -> None:
    # Allure attach для строк (url, method, raw response и т.п.)
    allure.attach(
        text,
        name=name,
        attachment_type=AttachmentType.TEXT,
    )
