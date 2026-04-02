from django import forms
from .models import TeacherProfile, ParentProfile, StudentProfile
from accounts.models import User

class BaseUserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text="Leave blank to auto-generate")

class TeacherCreationForm(BaseUserCreationForm):
    class Meta:
        model = TeacherProfile
        fields = ['date_of_birth', 'joining_date', 'bio']

class ParentCreationForm(BaseUserCreationForm):
    class Meta:
        model = ParentProfile
        fields = ['address']

class StudentCreationForm(BaseUserCreationForm):
    class Meta:
        model = StudentProfile
        fields = ['parent', 'class_level', 'section', 'roll_number', 'date_of_birth']
