from django.db import models

class FeeStructure(models.Model):
    class_level = models.ForeignKey('academics.ClassLevel', on_delete=models.CASCADE)
    academic_session = models.ForeignKey('academics.AcademicSession', on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=100)  # Tuition, Library, Transport, etc.
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class StudentFeePayment(models.Model):
    student = models.ForeignKey('people.StudentProfile', on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    academic_session = models.ForeignKey('academics.AcademicSession', on_delete=models.SET_NULL, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    month = models.IntegerField()  # 1 to 12
    is_confirmed = models.BooleanField(default=False)