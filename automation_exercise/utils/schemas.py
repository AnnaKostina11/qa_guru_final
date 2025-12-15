# Схема для GET /brandsList
# Проверяем, что:
# - есть responseCode
# - brands — массив и не пустой
# - у каждого элемента brands есть поле brand (непустая строка)
BRANDS_LIST_SCHEMA = {
    "type": "object",
    "required": ["responseCode", "brands"],
    "properties": {
        "responseCode": {"type": "integer"},
        "brands": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["brand"],
                "properties": {
                    "id": {"type": ["integer", "string"]},
                    "brand": {"type": "string", "minLength": 1},
                },
                "additionalProperties": True,
            },
        },
    },
    "additionalProperties": True,
}

# Универсальная схема для ответов вида:
# {"responseCode": <int>, "message": <str>}
# Используется в create/update/delete/verifyLogin.
MESSAGE_ONLY_SCHEMA = {
    "type": "object",
    "required": ["responseCode", "message"],
    "properties": {
        "responseCode": {"type": "integer"},
        "message": {"type": ["string", "object"]},
    },
    "additionalProperties": True,
}
