from django.shortcuts import redirect

class ForceProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.user.is_authenticated:
            profile = getattr(request.user, "profile", None)

            # Check if Google signaled that setup is required
            if request.session.get("force_complete_profile"):

                # If the user has NOT filled out required fields
                if not profile.role:  # adjust field name
                    if request.path != "/users/complete-profile/":
                        return redirect("complete_profile")

                # Once completed, remove the flag
                request.session.pop("force_complete_profile", None)

        return self.get_response(request)
