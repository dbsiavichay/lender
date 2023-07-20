from django.db import models

from .enums import CustomerStatus


class Customer(models.Model):
    external_id = models.CharField(unique=True, max_length=64)
    score = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.PositiveSmallIntegerField(
        choices=CustomerStatus.choices, default=CustomerStatus.ACTIVE
    )
