# automation_exercise/data/api_responses.py
# Модели (dataclass) для десериализации ответов API в типизированные объекты.
# Используются в BaseTestRequests.check_response(..., model_cls=...), чтобы тесты работали одинаково
# и не обращались к ответам как к "сырым" dict.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class MessageOnlyResponse:
    # Универсальная модель для ответов вида:
    # {"responseCode": <int>, "message": <str>}
    responseCode: int
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MessageOnlyResponse":
        # Приводим типы к ожидаемым (int/str), чтобы тесты не зависели от формата парсинга.
        return cls(
            responseCode=int(data.get("responseCode")),
            message=str(data.get("message")),
        )


@dataclass(frozen=True, slots=True)
class BrandItem:
    # Элемент списка брендов из /brandsList.
    # id может приходить как int или str (зависит от API/парсера).
    brand: str
    id: int | str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BrandItem":
        # brand приводим к строке; если поля нет — будет пустая строка (потом это ловится ассертами/схемой).
        return cls(
            id=data.get("id"),
            brand=str(data.get("brand", "")),
        )


@dataclass(frozen=True, slots=True)
class BrandsListResponse:
    # Модель для ответа /brandsList:
    # {"responseCode": <int>, "brands": [ { ... }, ... ]}
    responseCode: int
    brands: list[BrandItem]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BrandsListResponse":
        # Защищаемся от невалидного типа brands (например, если API вернул строку/объект).
        brands_raw = data.get("brands") or []
        if not isinstance(brands_raw, list):
            brands_raw = []

        return cls(
            responseCode=int(data.get("responseCode")),
            # Фильтруем только dict-элементы и превращаем их в BrandItem.
            brands=[BrandItem.from_dict(item) for item in brands_raw if isinstance(item, dict)],
        )
