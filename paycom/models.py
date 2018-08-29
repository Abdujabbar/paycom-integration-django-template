from django.db import models
# Create your models here.
class Transaction(models.Model):
    paycom_transaction_id = models.CharField(max_length=25, blank=False)
    paycom_time = models.CharField(max_length=13, blank=False)
    paycom_time_datetime=models.DateField(blank=False)
    create_time=models.DateField(blank=False)
    perform_time=models.DateField(blank=False)
    cancel_time=models.DateField(blank=False)
    amount=models.IntegerField(blank=False)
    state=models.SmallIntegerField(blank=False)
    reason=models.SmallIntegerField(blank=False)
    receivers=models.CharField(max_length=500, blank=False)
    order_id=models.IntegerField(blank=False)