import json
import allure
from allure_commons.types import AttachmentType


def attach_json(name: str, data) -> None:
    allure.attach(
        json.dumps(data, ensure_ascii=False, indent=2),
        name=name,
        attachment_type=AttachmentType.JSON,
    )


def attach_text(name: str, text: str) -> None:
    allure.attach(text, name=name, attachment_type=AttachmentType.TEXT)
