from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.forms import ValidationError
from django.db.models.fields.files import ImageFieldFile
from allauth.account.forms import SignupForm
from django import forms
from user.validators import validate_school_email

class CustomSignupForm(SignupForm):
    email = forms.EmailField(required=True, label="Email")

    def clean_email(self):
        email = self.cleaned_data["email"]
        validate_school_email(email)   # <-- apply validator manually
        return email

    def save(self, request):
        user = super().save(request)
        return user

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

    from django.core.files.uploadedfile import UploadedFile
    from django.forms import ValidationError
    from django.db.models.fields.files import ImageFieldFile

    def clean_image(self):
        image = self.cleaned_data.get('image')

        # If no new file uploaded, return existing image
        if not image or isinstance(image, ImageFieldFile):
            return image

        # -----------------------------
        # Validate only NEW uploaded files
        # -----------------------------
        # File size (limit 5MB)
        if image.size > 5 * 1024 * 1024:
            raise ValidationError("Image file too large ( > 5MB )")

        # File type (UploadedFile has content_type)
        if hasattr(image, 'content_type'):
            if not image.content_type.startswith('image/'):
                raise ValidationError("File is not an image")
        else:
            raise ValidationError("Invalid file upload")

        return image

