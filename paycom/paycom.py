from django.conf import settings
import json
from .exceptions import PaycomException
from paycom.behaviors.check_perform_transaction import CheckPerformTransaction
from paycom.behaviors.create_transaction import CreateTransaction
from paycom.behaviors.perform_transaction import PerformTransaction
from paycom.behaviors.cancel_transaction import CancelTransaction
from paycom.behaviors.check_transaction import CheckTransaction
from paycom.behaviors.get_statement import GetStatement
import base64


class Paycom(object):
    methods_dict = {
        'CheckPerformTransaction': 'check_perform_transaction',
        'CreateTransaction': 'create_transaction',
        'PerformTransaction': 'perform_transaction',
        'CancelTransaction': 'cancel_transaction',
        'CheckTransaction': 'check_transaction',
        'GetStatement': 'get_statement'
    }

    def __init__(self, request):
        self.key = settings.PAYCOM_API_KEY
        self.login = settings.PAYCOM_API_LOGIN
        self.request = request
        body = json.loads(request.body.decode('utf-8'))
        self.method = body['method']
        self.params = body['params']
        self.login = settings.PAYCOM_API_LOGIN

    def authorize(self):
        if 'HTTP_AUTHORIZATION' not in self.request.META:
            raise PaycomException(
                "UNAUTHENTICATED"
            )

        basic = self.request.META['HTTP_AUTHORIZATION']
        password = str(basic.replace("Basic", "")).strip()
        decoded = base64.b64decode(password)
        if self.generate_pair_login_pass().encode() != decoded:
            raise PaycomException(
                "UNAUTHENTICATED"
            )

        return True

    def generate_pair_login_pass(self):
        return self.login + ":" + self.key

    def launch(self):

        self.authorize()

        if self.method == "CheckPerformTransaction":
            return self.check_perform_transaction()
        elif self.method == "CreateTransaction":
            return self.create_transaction()
        elif self.method == "PerformTransaction":
            return self.perform_transaction()
        elif self.method == "CancelTransaction":
            return self.cancel_transaction()
        elif self.method == "CheckTransaction":
            return self.check_transaction()
        elif self.method == "GetStatement":
            return self.get_statement()

    def check_perform_transaction(self):
        behavior = CheckPerformTransaction(self.params)
        if behavior.execute():
            return {
                "result": {
                    "allow": True
                }
            }

    def create_transaction(self):
        behavior = CreateTransaction(self.params)
        transaction = behavior.execute()
        return {
            "result": {
                "created_time": transaction.create_time,
                "transaction": transaction.pk,
                "state": transaction.state,
            }
        }

    def perform_transaction(self):
        behavior = PerformTransaction(self.params)
        transaction = behavior.execute()
        return {
            "result": {
                "transaction": transaction.transaction,
                "perform_time": transaction.perform_time,
                "state": transaction.state,
            }
        }

    def cancel_transaction(self):
        behavior = CancelTransaction(self.params)
        transaction = behavior.execute()
        return {
            "result": {
                "transaction": transaction.transaction,
                "cancel_time": transaction.cancel_time,
                "state": transaction.state,
            }
        }

    def check_transaction(self):
        behavior = CheckTransaction(self.params)
        transaction = behavior.execute()
        return {
            "result": {
                "created_time": transaction.create_time,
                "perform_time": transaction.perform_time,
                "cancel_time": transaction.cancel_time,
                "transaction": transaction.transaction,
                "state": transaction.state,
                "reason": transaction.reason,
            }
        }

    def get_statement(self):
        behavior = GetStatement(self.params)
        items = behavior.execute()
        return {
            "result": items
        }

    def change_password(self):
        pass
