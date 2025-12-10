from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from .models import Profile
from django.forms import ValidationError
from django.db.models.fields.files import ImageFieldFile
from allauth.account.forms import SignupForm
from django import forms
from user.validators import validate_school_email, validate_not_banned

class CustomSignupForm(SignupForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        help_text="Please use your @virginia.edu email."
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Force email to be required (overrides Allauth)
        self.fields["email"].required = True
        self.fields["email"].widget.attrs["required"] = "required"
    def clean_email(self):
        email = self.cleaned_data.get("email")
        validate_school_email(email)
        validate_not_banned(email)
        return email
    def save(self, request):
        user = super().save(request)
        return user
    

class RoleChoiceForm(forms.Form):
    ROLE_CHOICES = [
    ("student", "Student"),
    ("moderator", "Request Moderator Access"),
]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        label="Register as",
        required=True,
    )
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        validators=[validate_school_email],  # same validator as signup
        help_text='Please use your @virginia.edu email.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'info', 'is_student', 'nickname', 'bio', 'interests', 'is_image_public']
        widgets = {
            'info': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Your biography...'
            }),
            'interests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What are you into?'
            }),
            'is_student': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')

        # No new upload → allow existing image
        if not image or isinstance(image, ImageFieldFile):
            return image

        # Validate file size (limit 5MB)
        if hasattr(image, 'size') and image.size > 5 * 1024 * 1024:
            raise ValidationError("Image file too large ( > 5MB )")

        # Validate image type safely
        content_type = getattr(image, 'content_type', None)
        if content_type and not content_type.startswith('image/'):
            raise ValidationError("File is not an image")

        return image

def profile_view(request, username): # For when you want to view a user's profile for the future
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile

    if not profile.is_image_public and request.user != profile_user:
        profile.image = None  # hide image
    return render(request, ...)
