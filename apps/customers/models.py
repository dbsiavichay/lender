from decimal import Decimal
from functools import cached_property

from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce

from apps.loans.enums import LoanStatus

from .enums import CustomerStatus


class Customer(models.Model):
    external_id = models.CharField(unique=True, max_length=64)
    score = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.PositiveSmallIntegerField(
        choices=CustomerStatus.choices, default=CustomerStatus.ACTIVE
    )

    def __str__(self):
        return self.external_id

    @cached_property
    def total_debt(self):
        result = self.loans.filter(
            status__in=[LoanStatus.PENDING, LoanStatus.ACTIVE]
        ).aggregate(total=Coalesce(Sum("outstanding"), Decimal(0)))

        return result.get("total")

    @cached_property
    def available_amount(self):
        return self.score - self.total_debt
