from django.db import models
from django.contrib.auth.models import User
import secrets
import hashlib


class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=100, help_text="A descriptive name for this API key")
    key_hash = models.CharField(max_length=64, unique=True, help_text="Hashed version of the API key")
    prefix = models.CharField(max_length=8, help_text="First 8 characters of the key for identification")
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"
    
    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.prefix}...)"
    
    @classmethod
    def generate_key(cls, user, name):
        """
        Generate a new API key for a user.
        Returns a tuple of (api_key_instance, raw_key)
        The raw_key should be shown to the user only once.
        """
        # Generate a secure random key
        raw_key = f"ep_{secrets.token_urlsafe(32)}"
        
        # Create hash of the key for storage
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        
        # Store first 8 characters as prefix for identification
        prefix = raw_key[:8]
        
        # Create the API key instance
        api_key = cls.objects.create(
            user=user,
            name=name,
            key_hash=key_hash,
            prefix=prefix
        )
        
        return api_key, raw_key
    
    @classmethod
    def validate_key(cls, raw_key):
        """
        Validate an API key and return the associated user if valid.
        Returns None if the key is invalid or inactive.
        """
        try:
            key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
            api_key = cls.objects.get(key_hash=key_hash, is_active=True)
            
            # Update last used timestamp
            from django.utils import timezone
            api_key.last_used_at = timezone.now()
            api_key.save(update_fields=['last_used_at'])
            
            return api_key.user
        except cls.DoesNotExist:
            return None
    
    def revoke(self):
        """Revoke this API key by setting it as inactive."""
        self.is_active = False
        self.save(update_fields=['is_active'])

