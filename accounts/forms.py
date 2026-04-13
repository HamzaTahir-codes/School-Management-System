from django import forms
from .models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'profile_picture', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make role field read-only during update as requested
        if self.instance and self.instance.pk:
            self.fields['role'].disabled = True
            self.fields['role'].required = False
