from django.db import models
from django.utils import timezone
from datetime import timedelta


class TenantManager(models.Manager):
    """Custom manager to filter queries by school (used with middleware)."""
    def for_school(self, school):
        return self.get_queryset().filter(school=school)


class TenantModel(models.Model):
    """Abstract base model for all tenant-scoped (school-specific) models."""
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name="%(class)s_related"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = TenantManager()

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['school']),
        ]


# Note: School model has been moved to apps/schools/models.py