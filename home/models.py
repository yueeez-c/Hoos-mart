from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
class Post(models.Model):

	title = models.CharField(max_length=100)
	date_posted = models.DateTimeField(auto_now=True)
	seller = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.title


# Create your models here.
