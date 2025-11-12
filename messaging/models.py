from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Thread(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='threads')
    context_listing = models.ForeignKey('Marketplace.Listing', null=True, blank=True,
                                        on_delete=models.SET_NULL, related_name='message_threads')
    created_at = models.DateTimeField(auto_now_add=True)

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

# Create your models here.
