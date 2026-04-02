from django import forms
from .models import TeacherAttendance, StudentAttendance, LeaveRequest

class TeacherAttendanceForm(forms.ModelForm):
    class Meta:
        model = TeacherAttendance
        fields = ['teacher', 'date', 'is_present']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class StudentAttendanceForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        fields = ['student', 'date', 'is_present', 'teacher']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['teacher', 'student', 'start_date', 'end_date', 'reason', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
