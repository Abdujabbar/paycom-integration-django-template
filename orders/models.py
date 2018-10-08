from django.db import models
from paycom.exceptions import PaycomException


class Order(models.Model):
    ORDER_ON_WAIT = 1
    ORDER_IS_PAYED = 2
    ORDER_CANCELLED = -1

    product_ids = models.CharField(max_length=255, blank=False)
    amount = models.BigIntegerField(blank=False)
    state = models.SmallIntegerField(blank=False)
    user_id = models.IntegerField(blank=False)
    phone = models.CharField(max_length=15, blank=False)

    def on_wait(self):
        return self.state == self.ORDER_ON_WAIT

    def is_payed(self):
        return self.state == self.ORDER_IS_PAYED

    def is_cancelled(self):
        return self.state == self.ORDER_CANCELLED

    def set_payed(self):
        self.state = self.ORDER_IS_PAYED
        self.save()

    def cancel(self):
        self.state = self.ORDER_CANCELLED
        self.save()

    @staticmethod
    def find_by_pk(pk):
        try:
            order = Order.objects.get(pk=pk)
            return order
        except Order.DoesNotExist as e:
            raise PaycomException("ORDER_NOT_FOUND")
