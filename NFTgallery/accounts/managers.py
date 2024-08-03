from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, password, username):
        if not phone:
            return ValueError('you didnt enter phone number')

        user = self.model(phone=phone, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, username):
        user = self.create_user(phone, password, username)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
