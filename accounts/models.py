from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid

from .manager import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(max_length=180, verbose_name="Email", unique=True)
    referral_code = models.CharField(max_length=128, default=None, verbose_name="کد معرف", null=True, blank=True)
    user_referral_code = models.CharField(default=uuid.uuid4(), unique=True,
                                          max_length=128, verbose_name="کد معرف کاربر", null=True)
    is_admin = models.BooleanField(default=False, verbose_name="Admin")
    is_active = models.BooleanField(default=True, verbose_name="active")
    created = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['referral_code']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        app_label = "accounts"
        # db_table = "User"
        db_table_comment = "custom user model with row attribute(AbstractBaseUser)"
        verbose_name = "User"
        verbose_name_plural = "Users"
