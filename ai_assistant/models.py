from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TenantModel


class AcademicContent(TenantModel):
    """Stores AI-generated content: schedules, outlines, exam papers, activities"""
    class ContentType(models.TextChoices):
        SCHEDULE = 'SCHEDULE', _('Class Schedule')
        OUTLINE = 'OUTLINE', _('Course Outline')
        EXAM_PAPER = 'EXAM_PAPER', _('Exam Paper')
        ACTIVITY = 'ACTIVITY', _('Daily Activity')

    content_type = models.CharField(max_length=20, choices=ContentType.choices)
    class_level = models.ForeignKey('academics.ClassLevel', on_delete=models.CASCADE)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, null=True, blank=True)
    data = models.JSONField()  # Flexible storage for AI output
    academic_session = models.ForeignKey('academics.AcademicSession', on_delete=models.CASCADE)