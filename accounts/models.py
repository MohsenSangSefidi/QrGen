from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.db import models


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class UserModel(AbstractUser):
    username = None
    nickname = models.CharField(_("Nickname"), max_length=150)
    email = models.EmailField(_("Email"), unique=True)
    api_key = models.CharField(
        _("API Key"), max_length=100, unique=True, default=get_random_string(length=100)
    )
    token = models.CharField(
        _("Token"), max_length=100, unique=True, default=get_random_string(length=100)
    )
    token_active_date = models.DateTimeField(
        _("Token Active Date"), default=timezone.now
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class QrCodeModel(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="qr_codes"
    )
    qrcode = models.ImageField(upload_to="qr_codes/")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.id
