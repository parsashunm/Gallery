from datetime import timedelta, datetime

import pytz
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from oauth2_provider.models import AbstractApplication
#
from .managers import UserManager
#


class User(AbstractBaseUser, PermissionsMixin):

    # base info
    username = models.CharField(max_length=128)
    phone = models.CharField(max_length=11, unique=True, db_index=True)
    about = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Auction
    participated_auction = models.PositiveIntegerField(default=0)
    won_auctions = models.PositiveIntegerField(default=0)

    # roles
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)

    objects = UserManager()

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'phone'

    def __str__(self):
        return f'{self.username} - {self.phone}'

    # def has_perm(self, perm, obj=None):
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     return True

    @property
    def is_staff(self):
        return self.is_admin

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if not hasattr(self, 'wallet'):
    #         Wallet.objects.create(owner=self)
    #     if not hasattr(self, 'card'):
    #         Card.objects.create(owner=self)
    #     if not hasattr(self, 'wishlist'):
    #         WishList.objects.create(owner=self)


    @property
    def auction_win_rate(self):
        return (self.won_auctions / self.participated_auction) * 100


class Wallet(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet', db_index=True)
    balance = models.PositiveIntegerField(default=0)
    blocked_balance = models.PositiveIntegerField(default=0)
    debt = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.owner.username}\'s wallet'


class OTP(models.Model):
    code = models.PositiveIntegerField()
    phone = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.code} | {self.phone} | {self.created_at}'

    def expire_code(self):
        rtime = self.created_at + timedelta(seconds=120)
        if datetime.now(tz=pytz.timezone('Asia/Tehran')) >= rtime:
            return True
        return False


class Role(models.Model):

    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.title


class Address(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    postal_code = models.IntegerField()
    address = models.TextField()

    class Meta:
        verbose_name_plural = 'addresses'
