from django.core.exceptions import ValidationError
from .models import BannedUser 

def validate_school_email(value):
    # Allow empty value (resend email POST)
    if not value:
        return

    domain = value.split("@")[-1].lower()

    if domain != "virginia.edu":
        raise ValidationError("Please use your @virginia.edu school email.")

def validate_school_email(value):
    # Allow empty value (resend email POST)
    if not value:
        return

    domain = value.split("@")[-1].lower()

    if domain != "virginia.edu":
        raise ValidationError("Please use your @virginia.edu school email.")


def validate_not_banned(value):
    """Prevent banned users from registering again."""
    if not value:
        return

    if BannedUser.objects.filter(email=value.lower()).exists():
        raise ValidationError("This email has been banned from the platform.")