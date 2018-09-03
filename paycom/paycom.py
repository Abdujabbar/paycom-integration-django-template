from .factory import MerchantFactory
from orders.models import Order
from .exceptions import PaycomException
from .models import Transaction
from .utils import time_now_in_ms
import json


class Paycom(object):

    def __init__(self, request):
        self.merchant = MerchantFactory.create_merchant(request)
        self.params = json.loads(request.body.decode('utf-8'))

    def launch(self):

        self.merchant.authorize()

        if self.params['method'] == "CheckPerformTransaction" and self.check_perform_transaction():
            return {
                "result": {
                    "allow": True
                }
            }

        if self.params['method'] == "CreateTransaction":
            transaction = self.create_transaction()
            return {
                "result": {
                    "created_time": transaction.create_time,
                    "transaction": transaction.transaction,
                    "state": transaction.state,
                }
            }

        if self.params['method'] == "PerformTransaction":
            transaction = self.perform_transaction()
            return {
                "result": {
                    "transaction": transaction.transaction,
                    "perform_time": transaction.perform_time,
                    "state": transaction.state,
                }
            }

        if self.params['method'] == "CancelTransaction":
            transaction = self.cancel_transaction()
            return {
                "result": {
                    "transaction": transaction.transaction,
                    "cancel_time": transaction.cancel_time,
                    "state": transaction.state,
                }
            }

        if self.params['method'] == "CheckTransaction":
            transaction = self.check_transaction()
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

        if self.params['method'] == "GetStatement":
            return {
                "result": self.get_statement()
            }

    def check_perform_transaction(self):

        if 'order_id' not in self.params['params']['account']:
            raise PaycomException("ORDER_NOT_FOUND")

        order = Order.find_by_pk(self.params['params']['account']['order_id'])


        if order.is_payed():
            raise PaycomException("ORDER_ALREADY_PAYED")

        if not order.on_wait():
            raise PaycomException("ORDER_CANCELLED")


        if self.params['params']['amount'] != order.amount:
            raise PaycomException("AMOUNTS_NOT_EQUALS")

        return True

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

        self.check_perform_transaction()

        transaction = Transaction()
        transaction.order_id = self.params['account']['order_id']
        transaction.time = self.params['time']
        transaction.transaction_id = self.params['id']
        transaction.account = self.params['account']['phone']
        transaction.amount = self.params['amount']
        transaction.create_time = time_now_in_ms()
        transaction.state = Transaction.STATE_CREATED
        transaction.transaction = self.params['account']['order_id']

        transaction.save()

        return transaction

    def perform_transaction(self):
        try:
            transaction = Transaction.find_by_pk(self.params['id'])

            if transaction.is_created():
                if transaction.is_timeout():
                    transaction.set_timed_out()
                    raise PaycomException("CANNOT_PERFORM_OPERATION")
            elif transaction.is_payed():
                return transaction

            order = Order.find_by_pk(self.params['account']['order_id'])
            order.set_payed()
            transaction.set_payed()
            return transaction

        except Exception as e:
            raise PaycomException("CANNOT_PERFORM_OPERATION")

    def cancel_transaction(self):
        transaction = Transaction.find_by_pk(self.params['id'])
        order = Order.find_by_pk(transaction.order_id)
        transaction.cancel(self.params['reason'])
        order.cancel()
        return transaction

    def check_transaction(self):
        transaction = Transaction.find_by_pk(self.params['id'])
        return transaction

    def get_statement(self):
        return Transaction.between(self.params['from'], self.params['to'])

    def change_password(self):
        pass
