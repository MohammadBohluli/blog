from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = "P", "Publish"
        DRAFT = "D", "Draft"

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    category = models.ManyToManyField("Category")
    content = models.TextField()
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.id


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
