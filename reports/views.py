from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Report
from marketplace.models import Listing
from messaging.models import Message
from .decorators import moderator_required
from user.models import Profile  

User = get_user_model()


# REPORT A LISTING
def report_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        description = request.POST.get("description", "").strip()

        if description:
            Report.objects.create(
                reporter=request.user,
                report_type="listing",
                reported_listing=listing,
                description=description
            )
            messages.success(request, "Thank you — your report has been submitted.")
            return redirect("listing-detail", listing_id=listing.id)

    return render(request, "reports/report_form.html", {
        "object": listing,
        "type": "listing"
    })


# REPORT A USER
def report_user(request, user_id):
    reported_user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        description = request.POST.get("reason", "").strip()

        if description:
            Report.objects.create(
                reporter=request.user,
                report_type="user",
                reported_user=reported_user,
                description=description
            )
            messages.success(request, "User reported.")
            return redirect("user-profile", user_id=reported_user.id)

    # >>> THIS MUST EXIST <<<
    return render(request, "reports/report_user_form.html", {
        "reported": reported_user,
        "type": "user"
    })
    


# REPORT A MESSAGE
def report_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if request.method == "POST":
        description = request.POST.get("description", "").strip()

        if description:
            Report.objects.create(
                reporter=request.user,
                report_type="message",
                reported_message=message,
                description=description
            )
            messages.success(request, "Message reported.")
            return redirect("messaging:conversations")

    return render(request, "reports/report_user_form.html", {
    "reported": message.sender,
    "type": "message"
})



# MODERATOR — VIEW ALL REPORTS
@moderator_required
def review_reports(request):
    reports = Report.objects.filter(is_resolved=False).order_by("-created_at")

    return render(request, "reports/review_reports.html", {
        "reports": reports,
    })


# ---------------------------
# MODERATOR — MARK RESOLVED
# ---------------------------
@moderator_required
def resolve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.is_resolved = True
    report.resolved_by = request.user
    report.save()

    messages.success(request, "Report marked as resolved.")
    return redirect("review-reports")


# ---------------------------
# MODERATOR — BAN A USER
# ---------------------------
@moderator_required
def ban_user(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if report.reported_user:
        user = report.reported_user
        user.is_active = False
        user.save()
        messages.success(request, "User has been banned.")

    return redirect("review-reports")


@moderator_required
def delete_listing(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if report.reported_listing:
        report.reported_listing.delete()
        messages.success(request, "Listing removed.")

    return redirect("review-reports")

@moderator_required
def approve_moderator(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.profile.is_moderator = True
    user.profile.moderator_approval_pending = False
    user.profile.save()
    messages.success(request, f"{user.username} is now a moderator.")
    return redirect("moderator-dashboard")

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