from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom User - Lives inside each tenant schema"""
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin / School Owner')
        TEACHER = 'TEACHER', _('Teacher')
        PARENT = 'PARENT', _('Parent')
        STUDENT = 'STUDENT', _('Student')

    role = models.CharField(max_length=10, choices=Role.choices)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/', blank=True, null=True)

    # Teacher-specific security
    force_password_change = models.BooleanField(default=False)
    default_password_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"