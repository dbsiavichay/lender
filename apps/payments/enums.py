from django.db import models


class PaymentStatus(models.IntegerChoices):
    COMPLETED = 1
    REJECTED = 2
