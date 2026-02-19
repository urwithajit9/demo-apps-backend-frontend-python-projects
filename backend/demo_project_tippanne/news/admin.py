from django.contrib import admin

from .models import News


@admin.register(News)
class NewsAdminClass(admin.ModelAdmin):
    list_display = ["title", "slug", "content", "created_at"]
