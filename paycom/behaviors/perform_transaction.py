from .base import BaseBehavior
from paycom.models import Transaction
from paycom.exceptions import PaycomException
from orders.models import Order


class PerformTransaction(BaseBehavior):
    def execute(self):
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
            return transaction

        except Exception as e:
            print(e)
            raise PaycomException("CANNOT_PERFORM_OPERATION")
