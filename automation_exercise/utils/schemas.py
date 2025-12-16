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
MESSAGE_ONLY_SCHEMA = {
    "type": "object",
    "required": ["responseCode", "message"],
    "properties": {
        "responseCode": {"type": "integer"},
        "message": {"type": ["string", "object"]},
    },
    "additionalProperties": True,
}

CREATE_ACCOUNT_REQUEST_SCHEMA = {
    "type": "object",
    "required": [
        "name",
        "email",
        "password",
        "title",
        "birth_date",
        "birth_month",
        "birth_year",
        "firstname",
        "lastname",
        "company",
        "address1",
        "address2",
        "country",
        "zipcode",
        "city",
        "state",
        "mobile_number",
    ],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "minLength": 3},
        "password": {"type": "string", "minLength": 1},
        "title": {"type": "string", "minLength": 1},
        "birth_date": {"type": ["string", "integer"]},
        "birth_month": {"type": ["string", "integer"]},
        "birth_year": {"type": ["string", "integer"]},
        "firstname": {"type": "string", "minLength": 1},
        "lastname": {"type": "string", "minLength": 1},
        "company": {"type": "string"},
        "address1": {"type": "string", "minLength": 1},
        "address2": {"type": "string"},
        "country": {"type": "string", "minLength": 1},
        "zipcode": {"type": "string", "minLength": 1},
        "city": {"type": "string", "minLength": 1},
        "state": {"type": "string", "minLength": 1},
        "mobile_number": {"type": "string", "minLength": 1},
    },
    "additionalProperties": True,
}

VERIFY_LOGIN_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["email", "password"],
    "properties": {
        "email": {"type": "string", "minLength": 3},
        "password": {"type": "string", "minLength": 1},
    },
    "additionalProperties": True,
}

DELETE_ACCOUNT_REQUEST_SCHEMA = VERIFY_LOGIN_REQUEST_SCHEMA

UPDATE_ACCOUNT_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["firstname", "lastname", "email", "password"],
    "properties": {
        "firstname": {"type": "string", "minLength": 1},
        "lastname": {"type": "string", "minLength": 1},
        "email": {"type": "string", "minLength": 3},
        "password": {"type": "string", "minLength": 1},
    },
    "additionalProperties": True,
}
