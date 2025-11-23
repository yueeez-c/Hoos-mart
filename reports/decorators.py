from django.http import HttpResponseForbidden

def moderator_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Not allowed")
        if not request.user.profile.is_moderator and not request.user.is_superuser:
            return HttpResponseForbidden("Moderator access only")
        return view_func(request, *args, **kwargs)
    return wrapper