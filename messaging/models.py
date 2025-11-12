# messaging/models.py
"""
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Thread(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='threads',
        through='ThreadParticipant'
    )

    participants_new = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ThreadParticipant",
        related_name="threads_new",
        blank=True,
    )

    context_listing = models.ForeignKey('Marketplace.Listing', null=True, blank=True,
                                        on_delete=models.SET_NULL, related_name='message_threads')
    created_at = models.DateTimeField(auto_now_add=True)

class ThreadParticipant(models.Model):
    thread = models.ForeignKey("Thread", on_delete=models.CASCADE, related_name="thread_participants")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="thread_participants")
    unread_count = models.PositiveIntegerField(default=0)
    last_seen = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("thread", "user")
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["thread"]),
        ]

class Message(models.Model):
    thread = models.ForeignKey('messaging.Thread', on_delete=models.CASCADE,
                               related_name='messages', null=True, blank=True)  # <-- allow null for backfill
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    listing = models.ForeignKey('Marketplace.Listing', null=True, blank=True,
                                on_delete=models.SET_NULL)
    is_system = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        who = getattr(self.sender, "username", str(self.sender))
        return f"{who}: {self.text[:40]}"
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    thread = models.ForeignKey('messaging.Thread', on_delete=models.CASCADE, null=True, blank=True)
    message = models.ForeignKey('messaging.Message', on_delete=models.CASCADE, null=True, blank=True)
    verb = models.CharField(max_length=120, default="sent you a message")  # keep simple
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "is_read", "created_at"])]

    def __str__(self):
        return f"Notif -> {self.user} ({'read' if self.is_read else 'unread'})"
"""
from django.db import models
from django.conf import settings

class Thread(models.Model):
    # OLD field (no through here!)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ThreadParticipant",
        related_name="threads",
        blank=True,
   )


    # NEW field with through
    participants_new = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ThreadParticipant",
        related_name="threads_new",
        blank=True,
    )

    context_listing = models.ForeignKey(
        'Marketplace.Listing', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='message_threads'
    )
    created_at = models.DateTimeField(auto_now_add=True)

class ThreadParticipant(models.Model):
    thread = models.ForeignKey("Thread", on_delete=models.CASCADE, related_name="thread_participants")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="thread_participants")
    unread_count = models.PositiveIntegerField(default=0)
    last_seen = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("thread", "user")
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["thread"]),
        ]

class Message(models.Model):
    thread = models.ForeignKey('messaging.Thread', on_delete=models.CASCADE,
                               related_name='messages', null=True, blank=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    listing = models.ForeignKey('Marketplace.Listing', null=True, blank=True,
                                on_delete=models.SET_NULL)
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
