from django.db import models
from django.conf import settings
from marketplace.models import Listing
from messaging.models import Message
from django.utils import timezone

class Report(models.Model):
    REPORT_TYPES = [
        ("listing", "Listing"),
        ("user", "User"),
        ("message", "Message"),
    ]
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports_made"
    )
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)

    # What is being reported
    listing = models.ForeignKey(Listing, null=True, blank=True, on_delete=models.SET_NULL)
    message = models.ForeignKey(Message, null=True, blank=True, on_delete=models.SET_NULL)
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        related_name="reports_against",
        on_delete=models.SET_NULL
    )

    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Report ({self.report_type}) by {self.reporter}"
