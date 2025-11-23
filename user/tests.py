from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import Profile

User = get_user_model()

class SignalHandlerTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_student_profile_created_on_signup(self):
        """Test that a student profile is created on signup."""
        # Create a user
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

        # Create a request and set the session data
        request = self.factory.get('/')
        request.session = {'desired_role': 'student'}

        # Manually send the signal
        user_signed_up.send(sender=self.__class__, request=request, user=user)

        # Check that a profile was created
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)
        self.assertTrue(profile.is_student)
        self.assertFalse(profile.moderator_approval_pending)

    def test_moderator_profile_created_on_signup(self):
        """Test that a moderator profile is created on signup."""
        # Create a user
        user = User.objects.create_user(username='moduser', email='mod@example.com', password='password')

        # Create a request and set the session data
        request = self.factory.get('/')
        request.session = {'desired_role': 'moderator'}

        # Manually send the signal
        user_signed_up.send(sender=self.__class__, request=request, user=user)

        # Check that a profile was created
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)
        self.assertFalse(profile.is_student)
        self.assertTrue(profile.moderator_approval_pending)

    def test_profile_creation_idempotent(self):
        """Test that the signal handler doesn't overwrite existing profile data."""
        # Create a user and an initial profile
        user = User.objects.create_user(username='existinguser', email='existing@example.com', password='password')
        profile = Profile.objects.create(user=user, is_student=True, moderator_approval_pending=False)

        # Create a request that would change the role
        request = self.factory.get('/')
        request.session = {'desired_role': 'moderator'}

        # Manually send the signal again
        user_signed_up.send(sender=self.__class__, request=request, user=user)

        # Get the profile and check that it hasn't changed
        profile.refresh_from_db()
        self.assertTrue(profile.is_student)
        self.assertFalse(profile.moderator_approval_pending)