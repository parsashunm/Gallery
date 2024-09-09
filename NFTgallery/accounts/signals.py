from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
#
from .models import (
    User, Role
)
#


@receiver(post_save, sender=User)
def set_default_role(sender, **kwargs):
    if kwargs['created'] and not kwargs['instance'].role:
        kwargs['instance'].role = Role.objects.get(title='buyer')
        kwargs['instance'].save()
