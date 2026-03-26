from django.db import models
from django.utils import timezone
from datetime import timedelta


class TenantManager(models.Manager):
    """Manager to filter queries by school (used with middleware)."""
    def for_school(self, school):
        return self.get_queryset().filter(school=school)


class TenantModel(models.Model):
    """Abstract base model for all tenant-scoped models."""
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name="%(class)s_related")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = TenantManager()

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['school']),
        ]


class School(models.Model):
    """School / Tenant"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    address = models.TextField()
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Subscription & Trial
    is_active = models.BooleanField(default=True)
    trial_ends_at = models.DateTimeField(default=timezone.now() + timedelta(days=2))
    subscription_plan = models.CharField(max_length=50, default='trial')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "School"
        verbose_name_plural = "Schools"