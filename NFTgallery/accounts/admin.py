from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUsrAdmin
# 
from .models import (
    User,
    OTP,
    Wallet,
    Role,
)
from .forms import UserCreationForm

# register accounts
admin.site.register(OTP)
admin.site.register(Wallet)
admin.site.register(Role)
#


# class UserRolesInLine(admin.TabularInline):
#     model = Role
#     extra = 1


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
