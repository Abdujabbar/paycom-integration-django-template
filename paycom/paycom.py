from django.conf import settings
from orders.models import Order
from .exceptions import PaycomException
from .models import Transaction
from .utils import time_now_in_ms
import json
import base64


class Paycom(object):
    methods = {
        "CheckPerformTransaction": "check_perform_transaction",
        "CreateTransaction": "create_transaction",
        "PerformTransaction": "perform_transaction",
        "CancelTransaction": "cancel_transaction",
        "CheckTransaction": "check_transaction",
        "GetStatement": "get_statement"
    }

    def __init__(self, request):
        body = json.loads(request.body.decode('utf-8'))
        self.method = body['method']
        self.params = body['params']
        self.request = request
        self.key = settings.PAYCOM_API_KEY
        self.login = settings.PAYCOM_API_LOGIN

    def authorize(self):
        if 'HTTP_AUTHORIZATION' not in self.request.META:
            raise PaycomException(
                "UNAUTHENTICATED"
            )

        basic = self.request.META['HTTP_AUTHORIZATION']
        password = str(basic.replace("Basic", "")).strip()
        decoded = base64.b64decode(password)
        login_key_pair = self.login + ":" + self.key
        if login_key_pair.encode() != decoded:
            raise PaycomException(
                "UNAUTHENTICATED"
            )
        return True

    def launch(self):

        self.authorize()
        m = getattr(self, self.methods[self.method])
        return m()

    def __check_perform_transaction(self):
        if 'order_id' not in self.params['account']:
            raise PaycomException("ORDER_NOT_FOUND")

        order = Order.find_by_pk(self.params['account']['order_id'])

        if order.is_payed():
            raise PaycomException("ORDER_ALREADY_PAYED")

        if not order.on_wait():
            raise PaycomException("ORDER_CANCELLED")

        if self.params['amount'] != order.amount:
            raise PaycomException("AMOUNTS_NOT_EQUALS")

        return True

    def check_perform_transaction(self):
        if self.__check_perform_transaction():
            return {
                "result": {
                    "allow": True
                }
            }

    def create_transaction(self):
        try:
            transaction = Transaction.find_by_pk(self.params['id'])

            if not transaction.is_created():
                raise PaycomException("CANNOT_PERFORM_OPERATION")

            if transaction.is_timeout():
                transaction.set_timed_out()
                raise PaycomException("CANNOT_PERFORM_OPERATION")

            return transaction
        except Exception as e:
            pass

        self.__check_perform_transaction()

        transaction_dict = {
            "order_id": self.params['account']['order_id'],
            "time": self.params['time'],
            "transaction_id": self.params['id'],
            "account": self.params['account']['phone'],
            "amount": self.params['amount'],
            "create_time": time_now_in_ms(),
            "state": Transaction.STATE_CREATED,
            "transaction": self.params['account']['order_id']
        }
        transaction = Transaction.objects.create(**transaction_dict)

        return {
            "result": {
                "created_time": transaction.create_time,
                "transaction": transaction.pk,
                "state": transaction.state,
            }
        }

    def perform_transaction(self):
        try:
            transaction = Transaction.find_by_pk(self.params['id'])

            if transaction.is_created():
                if transaction.is_timeout():
                    transaction.set_timed_out()
                    raise PaycomException("CANNOT_PERFORM_OPERATION")
            elif transaction.is_payed():
                return transaction

            order = Order.find_by_pk(transaction.order_id)
            order.set_payed()
            transaction.set_payed()

            return {
                "result": {
                    "transaction": transaction.transaction,
                    "perform_time": transaction.perform_time,
                    "state": transaction.state,
                }
            }
        except Exception as e:
            print(e)
            raise PaycomException("CANNOT_PERFORM_OPERATION")

    def cancel_transaction(self):
        transaction = Transaction.find_by_pk(self.params['id'])
        order = Order.find_by_pk(transaction.order_id)
        transaction.cancel(self.params['reason'])
        order.cancel()
        return {
            "result": {
                "transaction": transaction.transaction,
                "cancel_time": transaction.cancel_time,
                "state": transaction.state,
            }
        }

    def check_transaction(self):
        transaction = Transaction.find_by_pk(self.params['id'])
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
        return {
            "result": Transaction.objects.filter(create_time__gte=self.params['from'],
                                                 create_time__lte=self.params['to'])

        }

    def change_password(self):
        pass
