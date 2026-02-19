from rest_framework import serializers
from .models import DropBox

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["profile_picture"]


class DropBoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = DropBox
        fields = "__all__"
