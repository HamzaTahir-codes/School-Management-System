from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TenantModel


class TeacherProfile(TenantModel):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='teacher_profile')
    date_of_birth = models.DateField()
    joining_date = models.DateField()
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Teacher: {self.user.get_full_name() or self.user.username}"


class ParentProfile(TenantModel):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='parent_profile')
    address = models.TextField()
    is_fees_blocked = models.BooleanField(default=False)  # Will be updated by fees logic

    def __str__(self):
        return f"Parent: {self.user.get_full_name() or self.user.username}"


class StudentProfile(TenantModel):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        LEFT = 'LEFT', _('Left School')
        GRADUATED = 'GRADUATED', _('Graduated')

    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='student_profile')
    parent = models.ForeignKey('people.ParentProfile', on_delete=models.CASCADE, related_name='children')
    class_level = models.ForeignKey('academics.ClassLevel', on_delete=models.PROTECT)
    section = models.ForeignKey('academics.Section', on_delete=models.PROTECT)
    roll_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    admission_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        unique_together = ('school', 'roll_number', 'class_level')

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.class_level}"