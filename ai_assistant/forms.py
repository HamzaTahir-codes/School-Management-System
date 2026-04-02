from django import forms
from .models import AcademicContent

class AcademicContentForm(forms.ModelForm):
    class Meta:
        model = AcademicContent
        fields = ['content_type', 'class_level', 'subject', 'academic_session']
        # Note: data is a JSONField which handles generated data, usually not manually configured by standard forms.
