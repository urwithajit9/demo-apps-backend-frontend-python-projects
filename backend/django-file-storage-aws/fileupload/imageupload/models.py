from django.db import models

from storages.backends.s3 import S3File
from storages.backends.s3boto3 import S3Boto3Storage
from uuid import uuid4


class InvoiceFileS3Storage(S3Boto3Storage):
    location = "invoices"  # This will be the first suffix in a S3 path <s3>/invoices


def get_invoice_s3_file_path(instance: "Invoice", filename: str):
    return f"{uuid4().hex}.{filename.split('.')[-1]}"


class Invoice(models.Model):
    cost_center = models.CharField(max_length=255)
    generated_at = models.DateTimeField(auto_now_add=True)

    file = models.FileField(
        max_length=100,
        storage=InvoiceFileS3Storage,
        upload_to=get_invoice_s3_file_path,
    )

    def open(self) -> S3File:
        storage = InvoiceFileS3Storage()
        return storage.open(self.file.name, mode="rb")

    def __str__(self):
        return f"Invoice no.{self.id}"


class DropBox(models.Model):
    title = models.CharField(max_length=30)
    document = models.FileField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Drop Boxes"


from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )

    def __str__(self):
        return self.user.username
