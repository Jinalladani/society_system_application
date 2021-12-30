from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import date


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    otp = models.CharField(max_length=6, default=359)
    is_active = models.BooleanField(default=True)
    is_verfied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def create_superuser(self, phonenumber, password=None):
        user = self.model(
            phonenumber=phonenumber
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def __str__(self):
        return "{}".format(self.email)
