from django import forms
from .models import AcademicSession, ClassLevel, Section, Subject

class AcademicSessionForm(forms.ModelForm):
    class Meta:
        model = AcademicSession
        fields = ['name', 'start_date', 'end_date', 'is_current']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ClassLevelForm(forms.ModelForm):
    class Meta:
        model = ClassLevel
        fields = ['name', 'numeric_value']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['class_level', 'name', 'capacity']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'class_level']
