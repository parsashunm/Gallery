from django.db import models
from django.core.exceptions import ValidationError


class Treasury(models.Model):
    users_balance = models.PositiveIntegerField()
    profit = models.PositiveIntegerField()
