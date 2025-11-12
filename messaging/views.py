#messaging/views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect
from .models import Message, Thread
from django.db.models import Q
from Marketplace.models import Listing

User = get_user_model()

def login_required_view(request):
    return render(request, "messaging/login_required.html")

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, "messaging/user_list.html", {"users": users})

@login_required
def chat_view(request, other_user_id):
    other_user = get_object_or_404(User, pk=other_user_id)

    listing = None
    listing_id = request.GET.get("listing_id")
    if listing_id:
        listing = Listing.objects.filter(pk=listing_id).prefetch_related("images").first()

    # Find an existing thread that has *both* participants
    thread = (
        Thread.objects
        .filter(participants=request.user)
        .filter(participants=other_user)
        .distinct()
        .first()
    )
    if not thread:
        thread = Thread.objects.create()
        thread.participants.add(request.user, other_user)

    # Load messages for this thread
    messages_qs = (
        Message.objects
        .filter(thread=thread)
        .select_related("sender", "thread")
        .order_by("created_at")
    )

    return render(request, "messaging/chat.html", {
        "other_user": other_user,   # matches your template
        "listing": listing,         # for the banner and pinned line
        "chat_messages": messages_qs,    # used in the included chat_messages.html
        "thread": thread,           # handy if you need it in JS later
    })

@login_required
def chat_entry(request):
    # if someone hits /messaging/chat/ with no id, send them to the picker
    return redirect("messaging:user_list")


