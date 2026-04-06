from django.db import models
from django.utils.translation import gettext_lazy as _

class TeacherProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='teacher_profile')
    date_of_birth = models.DateField()
    joining_date = models.DateField()
    bio = models.TextField(blank=True)

    def get_active_assignments(self):
        from academics.models import TeacherAssignment, AcademicSession
        current_session = AcademicSession.objects.filter(is_current=True).first()
        return self.assignments.filter(academic_session=current_session) if current_session else self.assignments.none()

    def get_total_students_count(self):
        from people.models import StudentProfile
        assignments = self.get_active_assignments()
        sections = [a.section for a in assignments]
        return StudentProfile.objects.filter(section__in=sections).distinct().count()

    def __str__(self):
        return f"Teacher: {self.user.get_full_name() or self.user.username}"


class ParentProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='parent_profile')
    address = models.TextField()
    is_fees_blocked = models.BooleanField(default=False)  # Will be updated by fees logic

    def __str__(self):
        return f"Parent: {self.user.get_full_name() or self.user.username}"


class StudentProfile(models.Model):
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
        unique_together = ('roll_number', 'class_level')

    def get_attendance_stats(self):
        from attendance.models import StudentAttendance
        total = StudentAttendance.objects.filter(student=self).count()
        present = StudentAttendance.objects.filter(student=self, is_present=True).count()
        percentage = (present / total * 100) if total > 0 else 0
        return {
            'total': total,
            'present': present,
            'percentage': round(percentage, 1)
        }

    def get_fee_status(self):
        from fees.models import StudentFeePayment, FeeStructure
        from academics.models import AcademicSession
        
        current_session = AcademicSession.objects.filter(is_current=True).first()
        if not current_session:
            return {'total_due': 0, 'total_paid': 0, 'balance': 0}
            
        total_due = FeeStructure.objects.filter(
            class_level=self.class_level, 
            academic_session=current_session
        ).aggregate(models.Sum('amount'))['amount__sum'] or 0
        
        total_paid = StudentFeePayment.objects.filter(
            student=self, 
            academic_session=current_session,
            is_confirmed=True
        ).aggregate(models.Sum('amount_paid'))['amount_paid__sum'] or 0
        
        return {
            'total_due': total_due,
            'total_paid': total_paid,
            'balance': total_due - total_paid
        }

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.class_level}"

# Add to TeacherProfile
# (I will add them below the TeacherProfile class definition)