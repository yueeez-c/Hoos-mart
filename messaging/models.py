from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE, default=1)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE, default=1)
    content = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self): 
        return f'{self.sender}: {self.content}'

# Create your models here.
