from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("chat/<int:other_user_id>/", views.chat_view, name="chat"),
    path("notifications/dropdown/", views.notifications_dropdown, name="notifications-dropdown"),
    path("notifications/mark-read/", views.notifications_mark_all_read, name="notifications-mark-read"),
    path("contacts/", views.contacts_list, name="contacts"),
    path("conversations/", views.conversations_list, name="conversations"),
    path("", views.conversations_list, name="inbox"),
    path(
        "notifications/unread-count/",
        views.notifications_unread_count,
        name="notifications-unread-count",
    ),
]
