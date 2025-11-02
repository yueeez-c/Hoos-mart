from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("users/", views.user_list, name="user_list"),
    path("chat/<int:other_user_id>/", views.chat_view, name="chat"),
    path("login_required/", views.login_required_view, name="login_required"),
    path("chat/", views.chat_entry, name="chat_entry"),
]
