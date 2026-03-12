from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Extraction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField(max_length=2000)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Extraction from {self.url} at {self.timestamp}"


class Image(models.Model):
    extraction = models.ForeignKey(Extraction, on_delete=models.CASCADE, related_name='images')
    url = models.URLField(max_length=2000)
    name = models.CharField(max_length=255, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)  # Size in bytes
    file_type = models.CharField(max_length=50, blank=True)  # e.g., 'jpeg', 'png', 'gif'
    alt_text = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name or 'Unnamed'} from {self.extraction.url}"
    
    @property
    def dimensions(self):
        if self.width and self.height:
            return f"{self.width} x {self.height}"
        return "Unknown"
    
    @property
    def file_size_formatted(self):
        if self.file_size:
            if self.file_size < 1024:
                return f"{self.file_size} B"
            elif self.file_size < 1024 * 1024:
                return f"{self.file_size / 1024:.1f} KB"
            else:
                return f"{self.file_size / (1024 * 1024):.1f} MB"
        return "Unknown"

