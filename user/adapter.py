from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.urls import reverse
from allauth.exceptions import ImmediateHttpResponse
from .models import BannedUser

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.user.email
        if BannedUser.objects.filter(email=email).exists():
            # If the user is banned, prevent login and redirect
            raise ImmediateHttpResponse(redirect(reverse('banned_user_page')))

    # user/adapters.py
    from allauth.account.adapter import DefaultAccountAdapter
    class NoNewSignupEmailAdapter(DefaultAccountAdapter):
        def send_confirmation_mail(self, request, emailconfirmation, signup):
            # If this is a new signup, do NOTHING (suppress the email)
            if signup:
                return
            # If it's NOT a signup (e.g., a manual "Resend" request), send the email normally
            super().send_confirmation_mail(request, emailconfirmation, signup)
