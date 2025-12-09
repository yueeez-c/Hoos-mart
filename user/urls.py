from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("register/", views.choose_role, name="choose_role"),
    path("request-moderator/", views.request_moderator, name="request_moderator"),
    path("moderator/requests/", views.moderator_requests, name="moderator-requests"),
    path("moderator/approve/<int:profile_id>/", views.approve_moderator, name="approve-moderator"),
    path("moderator/deny/<int:profile_id>/", views.deny_moderator, name="deny-moderator"),
    path("<int:user_id>/", views.user_profile, name="user-profile"),
    path("banned/", views.banned_user_page, name="banned_user_page"),
]