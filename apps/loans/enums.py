from django.db import models


class LoanStatus(models.IntegerChoices):
    PENDING = 1
    ACTIVE = 2
    REJECTED = 3
    PAID = 4
