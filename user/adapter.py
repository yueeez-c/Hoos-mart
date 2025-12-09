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
