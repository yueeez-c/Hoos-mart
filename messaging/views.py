#messaging/views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect
from .models import Message, Thread, Notification, ThreadParticipant
from django.db.models import OuterRef, Subquery, Count, Q, F, Max
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
    # last message subqueries
    last_msg_qs = Message.objects.filter(thread=OuterRef("pk")).order_by("-created_at")
    last_msg_time = Subquery(last_msg_qs.values("created_at")[:1])
    last_msg_text = Subquery(last_msg_qs.values("text")[:1])
    last_msg_sender = Subquery(last_msg_qs.values("sender__username")[:1])

    # Threads where current user is a participant OR has sent a message,
    # and that actually have messages.
    base_qs = (
        Thread.objects
        .filter(
            Q(thread_participants__user=request.user) |
            Q(messages__sender=request.user)
        )
        .filter(messages__isnull=False)
        .annotate(
            last_msg_time=last_msg_time,
            last_msg_text=last_msg_text,
            last_msg_sender=last_msg_sender,
        )
        .prefetch_related("thread_participants__user", "messages__sender")
        .order_by("-last_msg_time", "-created_at")
        .distinct()
    )

    threads_raw = list(base_qs)

    # Collapse into one row per other_user
    summary_by_key = {}

    for t in threads_raw:
        # ---------- figure out other_user ----------
        other_user = None

        # 1) Try ThreadParticipant entries first
        others_from_participants = [
            tp.user
            for tp in t.thread_participants.all()
            if tp.user_id != request.user.id
        ]
        if others_from_participants:
            other_user = others_from_participants[0]

        # 2) Fallback: infer from senders in messages
        if other_user is None:
            sender_ids = {m.sender_id for m in t.messages.all()}
            sender_ids.discard(request.user.id)
            if sender_ids:
                other_user = User.objects.filter(id=list(sender_ids)[0]).first()

        # If we *still* don't know who the other person is, skip this legacy thread
        if other_user is None:
            continue

        t.other_user = other_user

        # ---------- grouping key (one row per other_user) ----------
        key = other_user.id
        current_time = t.last_msg_time or t.created_at

        best = summary_by_key.get(key)
        if best is None:
            summary_by_key[key] = t
        else:
            best_time = best.last_msg_time or best.created_at
            if current_time > best_time:
                summary_by_key[key] = t

    # Final list, sorted newest first
    threads = sorted(
        summary_by_key.values(),
        key=lambda t: t.last_msg_time or t.created_at,
        reverse=True,
    )

    return render(request, "messaging/conversations.html", {"threads": threads})

@login_required
def chat_view(request, other_user_id):
    other_user = get_object_or_404(User, pk=other_user_id)

    # Optional listing context
    listing = None
    listing_id = request.GET.get("listing_id")
    if listing_id:
        listing = Listing.objects.filter(pk=listing_id).prefetch_related("images").first()

    # Find existing thread with exactly these two users
    thread_qs = (
        Thread.objects
        .filter(thread_participants__user__in=[request.user, other_user])
        .annotate(num_participants=Count("thread_participants", distinct=True))
        .filter(num_participants=2)
    )

    if listing:
        thread_qs = thread_qs.filter(context_listing=listing)
    else:
        thread_qs = thread_qs.filter(context_listing__isnull=True)

    thread = thread_qs.first()

    # If none exists, create one + participants
    if thread is None:
        thread = Thread.objects.create(context_listing=listing)
        ThreadParticipant.objects.bulk_create([
            ThreadParticipant(thread=thread, user=request.user),
            ThreadParticipant(thread=thread, user=other_user),
        ])

    # Messages for THIS thread
    messages_qs = (
        Message.objects
        .filter(thread=thread)
        .select_related("sender", "thread")
        .order_by("created_at")
    )

    # 🔴 mark notifications for this thread as read for the current user
    Notification.objects.filter(
        user=request.user,
        thread=thread,
        is_read=False,
    ).update(is_read=True)

    # Sidebar threads list (optional – you can keep or later refactor)
    threads = (
        Thread.objects
        .filter(thread_participants__user=request.user)
        .annotate(last_msg=Max("messages__created_at"))
        .order_by("-last_msg", "-created_at")
        .distinct()
    )

    return render(request, "messaging/chat.html", {
        "other_user": other_user,
        "listing": listing,
        "chat_messages": messages_qs,
        "threads": threads,
        "thread": thread,
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


