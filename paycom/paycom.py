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

    def authorize(self):
        self.merchant.authorize()

    def check_perform_transaction(self):
        order_id = -1

        if 'order_id' not in self.params['account']:
            order_id = self.params['order_id']
        else:
            raise PaycomException("ORDER_NOT_FOUND")

        order = self.find_order()

        if order.is_payed():
            raise PaycomException("ORDER_ALREADY_PAYED")

        if self.params['amount'] != order.amount:
            raise PaycomException("AMOUNTS_NOT_EQUALS")

        return True

    def create_transaction(self):
        try:
            transaction = self.find_transaction()

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
            transaction = self.find_transaction()

            if transaction.is_created():
                if transaction.is_timeout():
                    transaction.set_timed_out()
                    raise PaycomException("CANNOT_PERFORM_OPERATION")
            elif transaction.is_payed():
                return transaction

            order = self.find_order()
            order.set_payed()
            transaction.state = Transaction.STATE_PAYED
            transaction.perform_time = time_now_in_ms()
            transaction.save()
            return transaction

        except Exception as e:
            raise PaycomException("CANNOT_PERFORM_OPERATION")


    def cancel_transaction(self):
        transaction = self.find_transaction()

        order = self.find_order()

        transaction.cancel()

        order.cancel()

        return transaction



    def check_transaction(self):
        transaction = self.find_transaction()
        return transaction

    def get_statement(self):
        return Transaction.between(self.params['from'], self.params['to'])


    def change_password(self):
        pass




    def find_transaction(self):
        try:
            transaction = Transaction.objects.get(self.params['id'])
            return transaction
        except Transaction.ObjectDoesNotExist as e:
            raise PaycomException("TRANSACTION_NOT_FOUND")

    def find_order(self):
        try:
            order = Order.objects.get(self.params['account']['order_id'])
            return order
        except Order.ObjectDoesNotExist as e:
            raise PaycomException("ORDER_NOT_FOUND")


