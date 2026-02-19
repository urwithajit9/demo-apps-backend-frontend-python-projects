# news/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django_tippanee.models import Comment


class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news")
    created_at = models.DateTimeField(auto_now_add=True)
    comments = GenericRelation(
        Comment
    )  # add comment from imported package django_trippanee

    def __str__(self):
        return self.title
