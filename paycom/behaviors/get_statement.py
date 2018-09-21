from .base import BaseBehavior
from paycom.models import Transaction


class GetStatement(BaseBehavior):
    def execute(self):
        return Transaction.between(self.params['from'], self.params['to'])
