from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse

class ForceProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.user.is_authenticated:
            # Check if the user is banned (is_active = False)
            if not request.user.is_active:
                logout(request)
                return redirect(reverse('banned_user_page'))

            profile = getattr(request.user, "profile", None)

            # If Google signaled that setup is required (this part of the original middleware remains)
            if request.session.get("force_complete_profile"):

                # If the user has NOT filled out required fields
                if not profile.role:  # adjust field name
                    if request.path != "/users/complete-profile/":
                        return redirect("complete_profile")

                # Once completed, remove the flag
                request.session.pop("force_complete_profile", None)

        return self.get_response(request)
