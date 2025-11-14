from allauth.account.signals import email_confirmed
from django.dispatch import receiver

@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    profile = user.profile
    profile.is_verified = True
    profile.save()
