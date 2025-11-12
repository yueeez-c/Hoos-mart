#messaging/views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect
from .models import Message, Thread, Notification, ThreadParticipant
from django.db.models import OuterRef, Subquery, Count, Q, F
from Marketplace.models import Listing
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.utils import timezone

User = get_user_model()

def login_required_view(request):
    return render(request, "messaging/login_required.html")

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, "messaging/user_list.html", {"users": users})

@login_required
def contacts_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, "messaging/contacts.html", {"users": users})

@login_required
def conversations_list(request):
    # annotate: last message time/text/sender and unread count per thread
    last_msg_time = Subquery(
        Message.objects.filter(thread=OuterRef('pk'))
        .order_by('-created_at').values('created_at')[:1]
    )
    last_msg_text = Subquery(
        Message.objects.filter(thread=OuterRef('pk'))
        .order_by('-created_at').values('text')[:1]
    )
    last_msg_sender = Subquery(
        Message.objects.filter(thread=OuterRef('pk'))
        .order_by('-created_at').values('sender__username')[:1]
    )
    # participant's last_read
    tp_last_read = Subquery(
        ThreadParticipant.objects.filter(thread=OuterRef('pk'), user=request.user)
        .values('last_read_at')[:1]
    )

    threads = (
        Thread.objects.filter(participants=request.user)
        .annotate(
            last_msg_time=last_msg_time,
            last_msg_text=last_msg_text,
            last_msg_sender=last_msg_sender,
            tp_last_read=tp_last_read,
            unread_count=Count(
                'messages',
                filter=Q(messages__created_at__gt=tp_last_read) & ~Q(messages__sender=request.user)
            )
        )
        .order_by('-last_msg_time', '-created_at')
    )

    return render(request, "messaging/conversations.html", {"threads": threads})

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

@login_required
def notifications_dropdown(request):
    notifs = (Notification.objects
              .filter(user=request.user)
              .select_related("message__sender", "thread")
              .order_by("-created_at")[:10])
    html = render_to_string("messaging/_notifications_dropdown.html",
                            {"notifs": notifs}, request=request)
    return HttpResponse(html)

@login_required
@require_POST
def notifications_mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({"ok": True})

@login_required
def notifications_unread_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({"count": count})


