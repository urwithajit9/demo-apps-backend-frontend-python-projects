from rest_framework import serializers
from django.contrib.auth.models import User
from extractor.models import Extraction, Image
from users.models import APIKey


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'url', 'name', 'size', 'width', 'height', 'format']


class ExtractionSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    image_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Extraction
        fields = ['id', 'url', 'status', 'timestamp', 'images', 'image_count']
        read_only_fields = ['id', 'timestamp', 'images', 'image_count']
    
    def get_image_count(self, obj):
        return obj.images.count()


class ExtractionCreateSerializer(serializers.Serializer):
    url = serializers.URLField()
    
    def validate_url(self, value):
        # Basic URL validation
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("URL must start with http:// or https://")
        return value


class APIKeySerializer(serializers.ModelSerializer):
    """Serializer for displaying API keys (without the actual key)"""
    
    class Meta:
        model = APIKey
        fields = ['id', 'name', 'prefix', 'created_at', 'last_used_at', 'is_active']
        read_only_fields = ['id', 'prefix', 'created_at', 'last_used_at']


class APIKeyCreateSerializer(serializers.Serializer):
    """Serializer for creating new API keys"""
    name = serializers.CharField(max_length=100, help_text="A descriptive name for this API key")
    
    def validate_name(self, value):
        # Check if user already has an API key with this name
        user = self.context['request'].user
        if APIKey.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError("You already have an API key with this name.")
        return value


class APIKeyResponseSerializer(serializers.Serializer):
    """Serializer for API key creation response (includes the raw key)"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    key = serializers.CharField(help_text="The API key - save this securely, it won't be shown again")
    prefix = serializers.CharField()
    created_at = serializers.DateTimeField()

