# apps/schools/forms.py
from django import forms
from django.core.validators import RegexValidator

class SchoolSignupForm(forms.Form):
    school_name = forms.CharField(max_length=255, label="School Name")
    slug = forms.CharField(
        max_length=50,
        label="School Slug (for subdomain)",
        validators=[
            RegexValidator(
                regex=r'^[a-z0-9-]+$',
                message="Slug can only contain lowercase letters, numbers and hyphens."
            )
        ],
        help_text="Example: abc-school"
    )
    email = forms.EmailField(label="Admin Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data