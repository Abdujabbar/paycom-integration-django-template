from django.db import models

# Create your models here.
class Order(models.Model):
    product_ids = models.CharField(max_length=255, blank=False)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=False)
    state = models.SmallIntegerField(blank=False)
    user_id = models.IntegerField(blank=False)
    phone = models.CharField(max_length=15, blank=False)