from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, **data):
        if not data['phone']:
            return ValueError('you didnt enter phone number')

        user = self.model(phone=data['phone'], username=data['username'])
        user.set_password(data['password'])
        user.save(using=self._db)
        return user

    def create_superuser(self, **data):
        user = self.create_user(**data)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
