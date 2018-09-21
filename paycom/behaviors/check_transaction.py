from .base import BaseBehavior
from paycom.models import Transaction


class CheckTransaction(BaseBehavior):
    def execute(self):
        transaction = Transaction.find_by_pk(self.params['id'])
        return transaction
