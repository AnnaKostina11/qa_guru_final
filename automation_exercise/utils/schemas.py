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

MESSAGE_ONLY_SCHEMA = {
    "type": "object",
    "required": ["responseCode", "message"],
    "properties": {
        "responseCode": {"type": "integer"},
        "message": {"type": "string"},
    },
    "additionalProperties": True,
}
