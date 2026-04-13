from django.db import models
from django.utils.translation import gettext_lazy as _

class AttendanceSettings(models.Model):
    start_time = models.TimeField(default='07:30:00')
    end_time = models.TimeField(default='08:15:00')
    allowed_ip_network = models.CharField(max_length=50, default='192.168.1.0/24', help_text="CIDR notation, e.g. 192.168.1.0/24")

    class Meta:
        verbose_name_plural = "Attendance Settings"

class TeacherAttendanceOTP(models.Model):
    teacher = models.ForeignKey('people.TeacherProfile', on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    request_ip = models.GenericIPAddressField(null=True, blank=True)

class TeacherAttendance(models.Model):
    teacher = models.ForeignKey('people.TeacherProfile', on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=True)
    time_marked = models.TimeField(auto_now_add=True, null=True)
    verified_by_otp = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_id = models.CharField(max_length=255, null=True, blank=True)
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