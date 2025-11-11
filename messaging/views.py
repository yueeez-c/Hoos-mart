from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect
from .models import Message
from django.db.models import Q

User = get_user_model()

def login_required_view(request):
    return render(request, "messaging/login_required.html")

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, "messaging/user_list.html", {"users": users})

@login_required
@login_required
def chat_view(request, other_user_id):
    if other_user_id == request.user.id:
        return redirect("messaging:user_list")

    other = get_object_or_404(User, id=other_user_id)

    # NEW: optional reference to a listing
    listing_id = request.GET.get("listing_id")
    listing = None
    if listing_id:
        from Marketplace.models import Listing
        listing = Listing.objects.filter(id=listing_id).first()

    msgs = (
        Message.objects
        .filter(Q(sender=request.user, receiver=other) | Q(sender=other, receiver=request.user))
        .select_related("sender", "receiver")
        .order_by("timestamp")[:100]
    )

    context = {
        "other_user": other,
        "chat_messages": msgs,
        "listing": listing,  # pass this to template
    }

    return render(request, "messaging/chat.html", context)

@login_required
def chat_entry(request):
    # if someone hits /messaging/chat/ with no id, send them to the picker
    return redirect("messaging:user_list")


