from django import forms
from .models import FeeStructure, StudentFeePayment

class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['class_level', 'academic_session', 'fee_type', 'amount']

class StudentFeePaymentForm(forms.ModelForm):
    class Meta:
        model = StudentFeePayment
        fields = ['student', 'amount_paid', 'month', 'is_confirmed']
