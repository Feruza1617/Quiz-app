from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.safestring import mark_safe
from rest_framework_simplejwt.tokens import RefreshToken


class AccountManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if phone is None:
            raise TypeError('Phone did not come')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        if not password:
            raise TypeError('Password did not come')
        user = self.create_user(phone, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


GENDER = (
    (0, "None"),
    (1, "Male"),
    (2, "Female"),
)


class Account(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=16, unique=True, db_index=True,
                             help_text="(995551133)")
    avatar = models.ImageField(upload_to='user/', validators=[], null=True, blank=True)
    gender = models.IntegerField(choices=GENDER, default=0)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_login = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()
    USERNAME_FIELD = 'phone'
    PHONE_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def str(self):
        if self.full_name:
            return self.full_name
        return self.phone

    def image_tag(self):
        if self.avatar:
            return mark_safe(f'<a href="{self.avatar.url}"><img src="{self.avatar.url}" style="height:50px;"/></a>')
        return 'no_image'

    @property
    def image_url(self):
        if self.avatar:
            if settings.DEBUG:
                return f'{settings.PROD_BASE_URL}{self.avatar.url}'
            return f'{settings.LOCAL_BASE_URL}{self.avatar.url}'

        else:
            return None

    @property
    def token(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'access': str(refresh.access_token)
        }
        return data
