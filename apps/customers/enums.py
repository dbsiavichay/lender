from django.db import models


class CustomerStatus(models.IntegerChoices):
    ACTIVE = 1
    INACTIVE = 2
