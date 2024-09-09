from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
#
from .models import (
    Treasury
)
#


@receiver(post_save, sender=Treasury)
def block_multi_treasury(sender, **kwargs):
    if kwargs['created']:
        raise ValidationError('na')
