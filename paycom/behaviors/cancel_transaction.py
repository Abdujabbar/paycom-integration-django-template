from .base import BaseBehavior
from paycom.models import Transaction
from orders.models import Order


class CancelTransaction(BaseBehavior):
    def execute(self):
        transaction = Transaction.find_by_pk(self.params['id'])
        order = Order.find_by_pk(transaction.order_id)
        transaction.cancel(self.params['reason'])
        order.cancel()
        return transaction
