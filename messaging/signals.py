# messaging/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def notify_on_message(sender, instance: Message, created, **kwargs):
    if not created:
        return
    if instance.is_system:
        return

    # notify everyone in the thread except the sender
    participants = instance.thread.participants.exclude(id=instance.sender_id)
    for u in participants:
        Notification.objects.create(
            user=u,
            thread=instance.thread,
            message=instance,
            verb="sent you a message",
        )
