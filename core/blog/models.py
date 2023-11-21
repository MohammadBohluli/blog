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
    slug = models.SlugField(max_length=255, unique_for_date='published_at')
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
        args = [self.published_at.year,self.published_at.month,self.published_at.day,self.slug]
        return reverse('blog:post_detail',args=args)
    
    


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created',]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"