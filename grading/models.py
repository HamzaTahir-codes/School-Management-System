from django.db import models
from core.models import TenantModel


class Mark(TenantModel):
    student = models.ForeignKey('people.StudentProfile', on_delete=models.CASCADE)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE)
    academic_session = models.ForeignKey('academics.AcademicSession', on_delete=models.CASCADE)
    teacher = models.ForeignKey('people.TeacherProfile', on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    term = models.CharField(max_length=50)  # Mid-term, Final, etc.

    class Meta:
        unique_together = ('student', 'subject', 'academic_session', 'term')


class FinalReport(TenantModel):
    """AI-aggregated final report for parents"""
    student = models.ForeignKey('people.StudentProfile', on_delete=models.CASCADE)
    academic_session = models.ForeignKey('academics.AcademicSession', on_delete=models.CASCADE)
    overall_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=5)
    teacher_remarks = models.TextField(blank=True)
    ai_summary = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)