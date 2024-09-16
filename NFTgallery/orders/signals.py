from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
#
from .models import (
    Treasury
)
#


@receiver(pre_save, sender=Treasury)
def block_multi_treasury(sender, **kwargs):
    treasuries = Treasury.objects.all()
    if treasuries.exists():
        if not treasuries.first().id == kwargs['instance'].id:
            raise ValidationError('we already have one dude')
