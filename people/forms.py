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
    profile_picture = forms.ImageField(required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email address already exists in the system.")
        return email

# ===================== CREATION FORMS =====================

class TeacherCreationForm(BaseUserCreationForm):
    class Meta:
        model = TeacherProfile
        fields = ['date_of_birth', 'joining_date', 'bio']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ParentCreationForm(BaseUserCreationForm):
    class Meta:
        model = ParentProfile
        fields = ['address']

class StudentCreationForm(BaseUserCreationForm):
    class Meta:
        model = StudentProfile
        fields = ['parent', 'class_level', 'section', 'roll_number', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

# ===================== UPDATE FORMS =====================

class BaseUserUpdateForm(forms.Form):
    """Handles the User-level fields during profile editing."""
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    profile_picture = forms.ImageField(required=False)

class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['date_of_birth', 'joining_date', 'bio']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['parent', 'class_level', 'section', 'roll_number', 'date_of_birth', 'status']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class ParentUpdateForm(forms.ModelForm):
    class Meta:
        model = ParentProfile
        fields = ['address']
