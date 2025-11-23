from django.db import models
from django.contrib.auth.models import User
import uuid

def user_directory_path(instance, filename):
    """Generate upload path for user files"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    filename = f"{uuid.uuid4()}.{ext}"
    # Return the path: uploads/user_<id>/<filename>
    return f'uploads/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    info = models.TextField(blank=True, null=True, default='')
    is_verified = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    moderator_approval_pending = models.BooleanField(default = False)

    def role_display(self):
        if self.is_moderator:
            return "Moderator"
        if self.moderator_approval_pending:
            return "Moderator (Pending Approval)"
    
        return "Student"

    def __str__(self):
        return f"{self.user.username}'s profile"

class UserFile(models.Model):
    """Demo model for showcasing S3 file uploads"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=user_directory_path)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
    @property
    def file_size_formatted(self):
        """Return human-readable file size"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

# Create your models here.
