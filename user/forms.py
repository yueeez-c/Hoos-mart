from django import forms
from .models import Profile

class StudentStatusForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['is_student']
        widgets = {
            'is_student': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')])
        }
