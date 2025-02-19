from django.contrib.auth.models import BaseUserManager

class MyUserManage(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Email must be provided!')
        if not username:
            raise ValueError('Username must be provided!')
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **kwargs):
        user = self.create_user(email, username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user