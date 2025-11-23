from rest_framework import serializers
from .models import Profile

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['nickname', 'bio', 'interests', 'image']

    # Example validations
    def validate_nickname(self, value):
        if value and len(value) > 50:
            raise serializers.ValidationError("Nickname must be under 50 characters.")
        return value

    def validate_bio(self, value):
        if value and len(value) > 1000:
            raise serializers.ValidationError("Bio is too long.")
        return value
