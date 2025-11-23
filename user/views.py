from django.contrib.auth import logout
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserUpdateForm, ProfileUpdateForm, RoleChoiceForm
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ProfileUpdateSerializer


def signup(request):
	if request.method == 'POST':
		form =UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account now has been created!')
			return redirect('login')
	else:
		form = UserCreationForm()
	return render(request,'user/signup.html', {'form':form})
	
@login_required
def profile(request):
    # Get or create profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Handle both user and profile forms
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            # Show success message with S3 info
            if 'image' in request.FILES:
                from django.conf import settings
                if hasattr(settings, 'AWS_STORAGE_BUCKET_NAME') and settings.AWS_STORAGE_BUCKET_NAME:
                    messages.success(request, f'Profile updated! Your image has been uploaded to S3.')
                else:
                    messages.success(request, f'Profile updated! Your image has been saved locally.')
            else:
                messages.success(request, f'Profile updated successfully!')
            
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    }
    return render(request, 'user/profile.html', context)
@login_required
def delete_profile(request):
    if request.method == "POST":
        user = request.user
        # Remove profile image if not default
        if hasattr(user, "profile"):
            img = user.profile.image
            if img and img.name != "profile_pics/default.jpg":
                img.delete(save=False)

        logout(request)
        user.delete()
        return redirect("/?deleted=1")

    return redirect("profile")

@login_required 
def s3_demo(request):
    """Demo page to showcase S3 file uploads"""
    from django.conf import settings
    from django.core.files.storage import default_storage
    from storages.backends.s3boto3 import S3Boto3Storage
    
    # S3 status information
    s3_info = {
        'configured': bool(getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)),
        'bucket_name': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'Not configured'),
        'storage_type': type(default_storage).__name__,
        'using_s3': isinstance(default_storage, S3Boto3Storage),
        'media_url': settings.MEDIA_URL
    }
    
    # Get all profiles with images to show examples
    profiles_with_images = Profile.objects.exclude(image='default.jpg').exclude(image='')[:10]
    
    context = {
        's3_info': s3_info,
        'profiles_with_images': profiles_with_images
    }
    
    return render(request, 'user/s3_demo.html', context)

class ProfileUpdateAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        profile = request.user.profile  # current user's profile

        serializer = ProfileUpdateSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def request_moderator(request):
    profile = request.user.profile

    # Prevent duplicates
    if profile.is_moderator:
        messages.info(request, "You are already a moderator.")
        return redirect("profile")

    if profile.moderator_approval_pending:
        messages.info(request, "Your request is already pending.")
        return redirect("profile")

    # Mark request as pending
    profile.moderator_approval_pending = True
    profile.save()

    messages.success(request, "Your request has been submitted!")
    return redirect("profile")

def choose_role(request):
    if request.method == "POST":
        form = RoleChoiceForm(request.POST)
        if form.is_valid():
            # Save choice in session so we can use it after signup
            request.session["desired_role"] = form.cleaned_data["role"]
            return redirect("account_signup")  # allauth's signup view
    else:
        form = RoleChoiceForm()

    return render(request, "user/choose_role.html", {"form": form})

def is_moderator(user):
    return user.is_superuser or user.profile.is_moderator

@login_required
@user_passes_test(is_moderator)
def moderator_requests(request):
    pending = Profile.objects.filter(moderator_approval_pending=True)

    return render(request, "user/moderator_requests.html", {"pending": pending})

@login_required
@user_passes_test(is_moderator)
def approve_moderator(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.is_moderator = True
    profile.moderator_approval_pending = False
    profile.save()

    messages.success(request, f"{profile.user.username} is now a moderator.")
    return redirect("moderator-requests")


@login_required
@user_passes_test(is_moderator)
def deny_moderator(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.moderator_approval_pending = False
    profile.save()

    messages.info(request, f"{profile.user.username}'s moderator request was denied.")
    return redirect("moderator-requests")


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)
    context = {
        'profile': profile
    }
    return render(request, 'user/user_profile.html', context)
