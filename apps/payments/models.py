import uuid

from django.db import models

from .enums import PaymentStatus


class Payment(models.Model):
    external_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    total_amount = models.DecimalField(max_digits=20, decimal_places=10)
    paid_at = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(
        choices=PaymentStatus.choices, default=PaymentStatus.COMPLETED
    )
    customer = models.ForeignKey("customers.Customer", on_delete=models.PROTECT)


class PaymentDetail(models.Model):
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    loan = models.ForeignKey("loans.Loan", on_delete=models.PROTECT)
    payment = models.ForeignKey("payments.Payment", on_delete=models.CASCADE)
