from django import forms
from .models import Mark, FinalReport

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'subject', 'academic_session', 'teacher', 'marks_obtained', 'max_marks', 'term']

class FinalReportForm(forms.ModelForm):
    class Meta:
        model = FinalReport
        fields = ['student', 'academic_session', 'overall_percentage', 'grade', 'teacher_remarks', 'ai_summary', 'is_published']
