from django.db import models
from django.utils.translation import gettext_lazy as _

class TeacherAttendance(models.Model):
    teacher = models.ForeignKey('people.TeacherProfile', on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=True)
    marked_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('teacher', 'date')


class StudentAttendance(models.Model):
    student = models.ForeignKey('people.StudentProfile', on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=True)
    teacher = models.ForeignKey('people.TeacherProfile', on_delete=models.SET_NULL, null=True, blank=True)


class LeaveRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')

    # Can be used by Teacher or Parent (for student)
    teacher = models.ForeignKey('people.TeacherProfile', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('people.StudentProfile', on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)