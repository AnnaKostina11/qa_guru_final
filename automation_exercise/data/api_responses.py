# automation_exercise/data/api_responses.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class MessageOnlyResponse:
    responseCode: int
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MessageOnlyResponse":
        return cls(
            responseCode=int(data.get("responseCode")),
            message=str(data.get("message")),
        )


@dataclass(frozen=True, slots=True)
class BrandItem:
    brand: str
    id: int | str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BrandItem":
        return cls(
            id=data.get("id"),
            brand=str(data.get("brand", "")),
        )


@dataclass(frozen=True, slots=True)
class BrandsListResponse:
    responseCode: int
    brands: list[BrandItem]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BrandsListResponse":
        brands_raw = data.get("brands") or []
        if not isinstance(brands_raw, list):
            brands_raw = []

        return cls(
            responseCode=int(data.get("responseCode")),
            brands=[BrandItem.from_dict(item) for item in brands_raw if isinstance(item, dict)],
        )
