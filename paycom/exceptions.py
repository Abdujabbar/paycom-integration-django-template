
class PaycomException(Exception):
    ERRORS = {
        "NOT_ALLOWED_METHOD": -32300,
        "JSON_PARSE":-32700,
        "WRONG_REQUEST_PARAMS":-32600,
        "METHOD_NOT_EXIST": -32601,
        "UNAUTHENTICATED": -32504,
        "SYSTEM_ERROR": -32400,
    }


