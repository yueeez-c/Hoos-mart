from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "is_student", "is_moderator", "moderator_approval_pending")
    list_filter = ("is_student", "is_moderator", "moderator_approval_pending")

admin.site.register(Profile, ProfileAdmin)