from django import forms
from .models import NotificationLog

class NotificationLogForm(forms.ModelForm):
    class Meta:
        model = NotificationLog
        fields = ['recipient', 'category', 'message', 'is_sent', 'sent_at']
        widgets = {
            'sent_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
