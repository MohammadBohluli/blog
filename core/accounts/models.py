from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name='ایمیل')
    first_name = models.CharField(max_length=255, verbose_name='نام')
    last_name = models.CharField(max_length=255, verbose_name='نام خانوادگی')
    is_staff = models.BooleanField(default=False, verbose_name='اجازه ورود به پنل مدیریت')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت فعال بودن کاربر')
    is_superuser = models.BooleanField(default=False, verbose_name='مدیر')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='بروزرسانی شده در')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def get_short_name(self):
        return self.first_name.strip().replace(" ","")
    
    def clean(self) -> None:
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
    
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
    
