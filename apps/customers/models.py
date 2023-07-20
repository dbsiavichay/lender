import uuid

from django.db import models

from .enums import CustomerStatus


class Customer(models.Model):
    external_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    score = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.PositiveSmallIntegerField(
        choices=CustomerStatus.choices, default=CustomerStatus.ACTIVE
    )
