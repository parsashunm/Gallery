from django.db import models
from django.core.exceptions import ValidationError


class Treasury(models.Model):
    title = models.CharField(max_length=32)
    users_balance = models.PositiveIntegerField(default=0)
    profit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
