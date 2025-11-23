# messaging/models.py
from django.db import models
from django.conf import settings

class Thread(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ThreadParticipant",
        related_name="threads",
        blank=True,
    )
    context_listing = models.ForeignKey(
        'marketplace.Listing', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='message_threads'
    )
    is_group = models.BooleanField(default=False, help_text="Whether this is a group conversation")
    group_name = models.CharField(max_length=100, blank=True, help_text="Name for group conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.is_group and self.group_name:
            return f"Group: {self.group_name}"
        return f"Thread {self.id}"

class ThreadParticipant(models.Model):
    thread = models.ForeignKey("Thread", on_delete=models.CASCADE, related_name="thread_participants")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="thread_participants")
    unread_count = models.PositiveIntegerField(default=0)
    last_seen = models.DateTimeField(null=True, blank=True)
    is_muted = models.BooleanField(default=False, help_text="Mute notifications for this conversation")
    is_archived = models.BooleanField(default=False, help_text="Archive this conversation")

    class Meta:
        unique_together = ("thread", "user")
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["thread"]),
            models.Index(fields=["user", "is_archived"]),
        ]

class Message(models.Model):
    thread = models.ForeignKey('messaging.Thread', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    listing = models.ForeignKey('marketplace.Listing', null=True, blank=True, on_delete=models.SET_NULL)
    is_system = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    thread = models.ForeignKey('messaging.Thread', on_delete=models.CASCADE, null=True, blank=True)
    message = models.ForeignKey('messaging.Message', on_delete=models.CASCADE, null=True, blank=True)
    verb = models.CharField(max_length=120, default="sent you a message")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "is_read", "created_at"])]
