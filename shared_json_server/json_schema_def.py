JSON_SCHEMA_REQUEST_METHOD_DEBUG_NOTIFY = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "debug notify method(A JSON RPC 2.0 request)",
    "type": "object",
    "required": [
        "method",
        "params"
    ],
    "not": {
        "required": [
            "id"
        ]
    },
    "properties": {
        "method": {
            "const": "debug_notify"
        },
        "params": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    }
}

JSON_SCHEMA_REQUEST_METHOD_ECHO = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "echo method(A JSON RPC 2.0 request)",
    "type": "object",
    "required": [
        "method",
        "params",
        "id"
    ],
    "properties": {
        "method": {
            "const": "echo"
        },
        "params": {
            "type": [
                "array",
                "object"
            ]
        }
    }
}

JSON_SCHEMA_REQUEST_METHOD_GET_DATA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "get data method(A JSON RPC 2.0 request)",
    "type": "object",
    "required": [
        "method",
        "params",
        "id"
    ],
    "properties": {
        "method": {
            "const": "get_data"
        },
        "params": {
            "type": "object",
            "required": [
                "data_name"
            ],
            "properties": {
                "data_name": {
                    "type": "string",
                    "pattern": "^/([A-Za-z0-9_,]+/)+$"
                },
                "lock_name": {
                    "type": "string"
                }
            }
        }
    }
}

JSON_SCHEMA_REQUEST_METHOD_SET_DATA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "set data method(A JSON RPC 2.0 request)",
    "type": "object",
    "required": [
        "method",
        "params",
        "id"
    ],
    "properties": {
        "method": {
            "const": "set_data"
        },
        "params": {
            "type": "object",
            "required": [
                "data_name",
                "data"
            ],
            "properties": {
                "data_name": {
                    "type": "string",
                    "pattern": "^/([A-Za-z0-9_,]+/)+$"
                },
                "lock_name": {
                    "type": "string"
                },
                "data": {
                    "type": [
                        "null",
                        "array",
                        "object"
                    ]
                }
            }
        }
    }
}

JSON_SCHEMA_REQUEST_METHOD_READ_DATA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "read data method(A JSON RPC 2.0 request)",
    "type": "object",
    "required": [
        "method",
        "params",
        "id"
    ],
    "properties": {
        "method": {
            "const": "read_data"
        },
        "params": {
            "type": "object",
            "required": [
                "data_name"
            ],
            "properties": {
                "data_name": {
                    "type": "string",
                    "pattern": "^/([A-Za-z0-9_,]+/)+$"
                },
                "lock_name": {
                    "type": "string"
                }
            }
        }
    }
}

JSON_SCHEMA_REQUEST_METHOD_WRITE_DATA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "write_data method(A JSON RPC 2.0 request)",
    "type": "object",
    "required": [
        "method",
        "params",
        "id"
    ],
    "properties": {
        "method": {
            "const": "write_data"
        },
        "params": {
            "type": "object",
            "required": [
                "data_name",
                "data"
            ],
            "properties": {
                "data_name": {
                    "type": "string",
                    "pattern": "^/([A-Za-z0-9_,]+/)+$"
                },
                "lock_name": {
                    "type": "string"
                },
                "data": {
                    "type": [
                        "null",
                        "array",
                        "object"
                    ]
                }
            }
        }
    }
}

JSON_SCHEMA_REQUEST_METHOD_LOCK = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "lock_data method(A JSON RPC 2.0 request)",
    "type": "object",
    "required": [
        "method",
        "params",
        "id"
    ],
    "properties": {
        "method": {
            "const": "lock_data"
        },
        "params": {
            "type": "object",
            "required": [
                "data_name",
                "lock_name"
            ],
            "properties": {
                "data_name": {
                    "type": "string",
                    "pattern": "^/([A-Za-z0-9_,]+/)+$"
                },
                "lock_name": {
                    "type": "string"
                }
            }
        }
    }
}

JSON_SCHEMA_REQUEST_METHOD_RELEASE = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "release_data method(A JSON RPC 2.0 request)",
    "type": "object",
    "required": [
        "method",
        "params",
        "id"
    ],
    "properties": {
        "method": {
            "const": "release_data"
        },
        "params": {
            "type": "object",
            "required": [
                "data_name",
                "lock_name"
            ],
            "properties": {
                "data_name": {
                    "type": "string",
                    "pattern": "^/([A-Za-z0-9_,]+/)+$"
                },
                "lock_name": {
                    "type": "string"
                }
            }
        }
    }
}

JSON_SCHEMA_REQUEST_METHOD_LIST = [
    JSON_SCHEMA_REQUEST_METHOD_LOCK,
    JSON_SCHEMA_REQUEST_METHOD_RELEASE,
    JSON_SCHEMA_REQUEST_METHOD_READ_DATA,
    JSON_SCHEMA_REQUEST_METHOD_WRITE_DATA,
    JSON_SCHEMA_REQUEST_METHOD_GET_DATA,
    JSON_SCHEMA_REQUEST_METHOD_SET_DATA
]
