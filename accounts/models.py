from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
  def get_by_natural_key(self, username):
    return self.get(username=username)

  def create_superuser(self, username, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser must have is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')

    return self._create_user(username, password, **extra_fields)

  def _create_user(self, username, password=None, **extra_fields):
    if not username:
      raise ValueError('The Username field must be set')
    user = self.model(username=username, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(verbose_name="ユーザーネーム", unique=True, max_length=100)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  objects = CustomUserManager()

  USERNAME_FIELD = 'username'