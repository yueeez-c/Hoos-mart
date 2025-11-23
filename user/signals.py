from django.dispatch import receiver
from allauth.account.signals import email_confirmed, user_signed_up
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    profile, created = Profile.objects.get_or_create(user=user)
    profile.is_verified = True
    profile.save()


@receiver(user_signed_up)
def populate_profile_on_signup(request, user, **kwargs):
    profile, created = Profile.objects.get_or_create(user=user)

    # User has just signed up — apply role from session
    role = request.session.get("desired_role", None)

    if role == "student":
        profile.is_student = True

    elif role == "moderator":
        profile.moderator_approval_pending = True

    profile.save()
