from pyexpat import model
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth import password_validation
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
import uuid

# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    This class is a manager for custom User model.
    """

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be Provided...")
        if not password:
            raise ValueError("Password must be Provided...")

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password, **extra_fields):
        """
        This function is create user with only is_active
        field True(Authenticated  user).
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        This function is create user with is_active, is_staff,
        is_superuser field True(Superuser).
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    This class is represent custom User model.
    """

    email = models.EmailField(unique=True, verbose_name="Email", primary_key=True)

    emp_name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_superuser = models.BooleanField(default=False, verbose_name="Superuser")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Holiday(models.Model):

    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    email = models.ForeignKey("User", on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.email.email
