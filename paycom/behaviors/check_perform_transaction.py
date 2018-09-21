from .base import BaseBehavior
from paycom.exceptions import PaycomException
from orders.models import Order


class CheckPerformTransaction(BaseBehavior):
    def execute(self):
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
