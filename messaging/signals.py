# messaging/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, ThreadParticipant

@receiver(post_save, sender=Message)
def notify_on_message(sender, instance: Message, created, **kwargs):
    if not created or instance.is_system or not instance.thread_id:
        return

    other_user_ids = (ThreadParticipant.objects
                      .filter(thread=instance.thread_id)
                      .exclude(user_id=instance.sender_id)
                      .values_list('user_id', flat=True))

    notifs = [
        Notification(
            user_id=uid,
            thread_id=instance.thread_id,
            message_id=instance.id,
            verb="sent you a message",
        )
        for uid in other_user_ids
    ]
    if notifs:
        Notification.objects.bulk_create(notifs, ignore_conflicts=True)
