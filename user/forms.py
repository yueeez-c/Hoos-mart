from django import forms
from django.contrib.auth.models import User
from .models import Profile

class StudentStatusForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['is_student']
        widgets = {
            'is_student': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')])
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'info', 'is_student']
        widgets = {
            'info': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'is_student': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Validate file size (limit to 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")
            
            # Validate file type
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError("File is not an image")
                
        return image
