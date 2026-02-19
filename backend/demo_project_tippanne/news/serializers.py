# news/serializers.py
from rest_framework import serializers
from .models import News
from django.contrib.auth.models import User
from django_tippanee.serializers import CommentSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class NewsSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ["id", "title", "slug", "content", "author", "created_at", "comments"]
