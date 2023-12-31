from django.db import models

from .enums import LoanStatus


class Loan(models.Model):
    external_id = models.CharField(unique=True, max_length=64)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    contract_version = models.CharField(max_length=32, blank=True, null=True)
    outstanding = models.DecimalField(max_digits=12, decimal_places=2)
    taken_at = models.DateTimeField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        choices=LoanStatus.choices, default=LoanStatus.ACTIVE
    )
    customer = models.ForeignKey(
        "customers.Customer", on_delete=models.PROTECT, related_name="loans"
    )
