
class PaycomException(Exception):
    code = 0
    message = ""

    ERRORS_CODES = {
        "NOT_ALLOWED_METHOD": -32300,
        "JSON_PARSE":-32700,
        "WRONG_REQUEST_PARAMS":-32600,
        "METHOD_NOT_EXIST": -32601,
        "UNAUTHENTICATED": -32504,
        "SYSTEM_ERROR": -32400,
        "CANNOT_PERFORM_OPERATION":-31008,

        "AMOUNTS_NOT_EQUALS": -31001,
        "TRANSACTION_NOT_FOUND": -31003,
        "ORDER_NOT_FOUND": -31050,
        "ORDER_ALREADY_PAYED": -31051,
    }
    ERROR_MESSAGES = {
        "UNAUTHENTICATED": {
            "ru": "Не авторизован",
            "uz": "Avtorizasiyadan o'tmagan",
            "en": "Unauthenticated",
        },
        "AMOUNTS_NOT_EQUALS": {
            "ru": "Суммы не совпадают",
            "uz": "To'lov summalari mos kelmadi",
            "en": "Amount not equals"
        },
        "CANNOT_PERFORM_OPERATION": {
            "ru": "Невозможно выполнить операцию.",
            "uz": "Operasiyani bajarib bo'lmadi",
            "en": "Can't perform operation"
        },
        "TRANSACTION_NOT_FOUND": {
            "ru": "Транзакция не найдена",
            "uz": "Tranzaksiya topilmadi",
            "en": "Transaction not found"
        }
    }


    def __init__(self, code):
        self.code = code
        self.message = self.ERROR_MESSAGES[code]


