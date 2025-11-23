from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("users/", views.user_list, name="user_list"),
    path("chat/", views.chat_entry, name="chat_entry"),
    path("chat/<int:other_user_id>/", views.chat_view, name="chat"),
    path("chat/<int:user_id>/", views.chat_view, name="chat"),
    path("login_required/", views.login_required_view, name="login_required"),
    path("notifications/dropdown/", views.notifications_dropdown, name="notifications-dropdown"),
    path("notifications/mark-read/", views.notifications_mark_all_read, name="notifications-mark-read"),
    path("contacts/", views.contacts_list, name="contacts"),
    path("conversations/", views.conversations_list, name="conversations"),
    path("chat/<int:other_user_id>/", views.chat_view, name="chat"),
    path("", views.conversations_list, name="inbox"),
    path(
        "notifications/unread-count/",
        views.notifications_unread_count,
        name="notifications-unread-count",
    ),
  
    
]
