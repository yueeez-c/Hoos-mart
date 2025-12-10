from django.urls import path
from . import views
urlpatterns = [
    path("report/listing/<int:listing_id>/", views.report_listing, name="report-listing"),
    path("user/<int:user_id>/", views.report_user, name="report-user"),
    path("message/<int:message_id>/", views.report_message, name="report-message"),
    # moderator pages
    path("resolve/<int:report_id>/", views.resolve_report, name="resolve-report"),
    path("moderator/delete-listing/<int:listing_id>/", views.delete_listing, name="delete-listing"),
    path("ban-user/<int:report_id>/", views.ban_user, name="ban-user"),
    path("approve/<int:report_id>/", views.approve_moderator, name="approve-moderator"),
    path("dashboard/", views.moderator_dashboard, name="moderator-dashboard"),
    path("review/", views.review_reports, name="review-reports"),
    path("view-user-profile/<int:user_id>/", views.view_user_profile, name="view-user-profile"),
]
