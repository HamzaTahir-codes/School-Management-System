from django import forms
from schools.models import School

class SchoolIdentityForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['tagline', 'about_text', 'mission', 'vision', 'logo']
        widgets = {
            'tagline': forms.TextInput(attrs={'class': 'w-full rounded-xl border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'about_text': forms.Textarea(attrs={'class': 'w-full rounded-xl border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500', 'rows': 4}),
            'mission': forms.Textarea(attrs={'class': 'w-full rounded-xl border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500', 'rows': 3}),
            'vision': forms.Textarea(attrs={'class': 'w-full rounded-xl border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500', 'rows': 3}),
        }
