from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUsrAdmin
from oauth2_provider.models import AccessToken
# 
from .models import (
    User, OTP, Wallet, Role, Address,
)
from .forms import UserCreationForm

# register accounts
admin.site.register(OTP)
#


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'balance']
    search_fields = ['owner__phone']


@admin.register(User)
class UserAdmin(BaseUsrAdmin):
    # form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'username', 'phone', 'is_verified')
    readonly_fields = ['last_login']
    list_filter = ['is_admin', 'is_verified']
    search_fields = ('username', 'phone')
    ordering = ('username',)

    fieldsets = [
        ('info',
         {
             'fields': [
                 'username',
                 'phone',
                 'password',

             ],
         }),
        ('perms',
         {
             'fields': [
                 'is_verified',
                 'is_active',
                 'is_admin',
                 'is_superuser',
                 'role',
                 'groups',
                 'user_permissions',
                 'last_login',
             ],
         })
    ]

    add_fieldsets = [
        ('None',
         {
             'fields': [
                 'username',
                 'phone',
                 'password',
                 'role',
             ],
         }),
    ]

    filter_horizontal = ('user_permissions', 'groups')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner']



