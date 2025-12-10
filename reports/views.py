from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth import get_user_model
from reports.decorators import moderator_required 
from reports.models import Report
from user.models import Profile, BannedUser 
from marketplace.models import Listing 
from django.shortcuts import get_object_or_404, redirect, render


User = get_user_model()


# REPORT A LISTING
def report_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    existing_report = Report.objects.filter(
        reporter=request.user,
        report_type="listing",
        listing=listing,
        is_resolved=False
    ).exists()

    if existing_report:
        messages.error(request, "You have already reported this listing and it is still under review.")
        return redirect("marketplace-buy")

    if request.method == "POST":
        description = request.POST.get("reason", "").strip()

        if description:
            Report.objects.create(
                reporter=request.user,
                report_type="listing",
                listing=listing,
                description=description,
            )
            messages.success(request, f"Listing '{listing.title}' has been reported.")
            return redirect("marketplace-buy")

        messages.error(request, "Please enter a reason.")

    return render(request, "reports/report_listing_form.html", {
        "reported": listing,
        "type": "listing",
    })

# REPORT A USER
def report_user(request, user_id):
    reported_user = get_object_or_404(User, id=user_id)

    # Prevent duplicate pending reports
    existing_report = Report.objects.filter(
        reporter=request.user,
        report_type="user",
        reported_user=reported_user,
        is_resolved=False
    ).exists()

    if existing_report:
        messages.error(request, "You already reported this user. The report is still being reviewed.")
        return redirect("messaging:contacts")

    if request.method == "POST":
        description = request.POST.get("reason", "").strip()

        if description:
            Report.objects.create(
                reporter=request.user,
                report_type="user",
                reported_user=reported_user,
                description=description
            )
            messages.success(request, f"User {reported_user.username} has been reported.")
            return redirect("messaging:contacts")
        
    return render(request, "reports/report_user_form.html", {
        "reported": reported_user,
        "type": "user"
    })
    


# REPORT A MESSAGE
def report_message(request, message_id):
    message_obj = get_object_or_404(Message, id=message_id)

    existing_report = Report.objects.filter(
        reporter=request.user,
        report_type="message",
        message=message_obj,
        is_resolved=False
    ).exists()

    if existing_report:
        messages.error(request, "You already reported this message and it is still pending review.")
        return redirect("messaging:contacts")

    if request.method == "POST":
        description = request.POST.get("reason", "").strip()

        if description:
            Report.objects.create(
                reporter=request.user,
                report_type="message",
                message=message_obj,
                description=description,
            )
            messages.success(request, "Message reported.")
            return redirect("messaging:contacts")

    return render(...)


# MODERATOR — VIEW ALL REPORTS
@moderator_required
def review_reports(request):
    reports = Report.objects.filter(is_resolved=False).order_by("-created_at")

    return render(request, "reports/review_reports.html", {
        "reports": reports,
    })


@moderator_required
def resolve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.is_resolved = True
    report.resolved_by = request.user
    report.save()

    messages.success(request, "Report marked as resolved.")
    return redirect("moderator-dashboard")


@moderator_required
def ban_user(request, report_id):

    report = get_object_or_404(Report, id=report_id)

    user = report.reported_user

    if user:
    
        if not BannedUser.objects.filter(email=user.email).exists():
            BannedUser.objects.create(email=user.email)
        
        user.is_active = False
        user.save()

    
        from django.contrib.sessions.models import Session
        Session.objects.filter(session_key__in=[session.session_key for session in Session.objects.all() if session.get_decoded().get('_auth_user_id') == str(user.id)]).delete()


        from messaging.models import ThreadParticipant
        ThreadParticipant.objects.filter(user=user).delete()

        report.is_resolved = True
        report.resolved_by = request.user
        report.save()

        Report.objects.filter(reported_user=user, is_resolved=False).exclude(id=report.id).delete()

        messages.success(request, f"User {user.username} has been banned, all active sessions terminated, and related reports resolved.")
    else:
        messages.error(request, "No reported user found for this report.")

    return redirect("moderator-dashboard")



@moderator_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    Report.objects.filter(listing=listing).delete()

    listing.delete()

    messages.success(request, "Listing and all related reports have been removed.")
    return redirect("moderator-dashboard")

@moderator_required
def approve_moderator(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        user.profile.is_moderator = True
        user.profile.moderator_approval_pending = False
        user.profile.save()

        messages.success(request, f"{user.username} is now a moderator.")
        return redirect("moderator-dashboard")
    
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("moderator-dashboard")

@moderator_required
def deny_moderator(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        user.profile.is_moderator = False
        user.profile.moderator_approval_pending = False
        user.profile.save()

        messages.success(request, f"{user.username} denied moderator access.")
        return redirect("moderator-dashboard")
    
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("moderator-dashboard")


@moderator_required
def view_user_profile(request, user_id):
    return redirect("user-profile", user_id=user_id)

@moderator_required
def moderator_dashboard(request):
    # Moderator approval requests
    pending_requests = Profile.objects.filter(
        moderator_approval_pending=True,
        is_moderator=False
    )

    # Reported content
    reported_listings = Report.objects.filter(
        report_type="listing", is_resolved=False
    )
    reported_messages = Report.objects.filter(
        report_type="message", is_resolved=False
    )
    reported_users = Report.objects.filter(
        report_type="user", is_resolved=False
    )

    context = {
        "pending_requests": pending_requests,
        "reported_listings": reported_listings,
        "reported_messages": reported_messages,
        "reported_users": reported_users,
    }

    return render(request, "reports/moderator_dashboard.html", context)