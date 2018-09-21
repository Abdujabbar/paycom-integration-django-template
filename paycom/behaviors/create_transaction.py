from .base import BaseBehavior
from paycom.models import Transaction
from paycom.exceptions import PaycomException
from paycom.behaviors.check_perform_transaction import CheckPerformTransaction
from paycom.utils import time_now_in_ms


class CreateTransaction(BaseBehavior):
    def execute(self):
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

        check_perform = CheckPerformTransaction(self.params)
        check_perform.execute()

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

        return Transaction.objects.create(**transaction_dict)
