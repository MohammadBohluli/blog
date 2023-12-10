from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from django.urls import reverse



class Post(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = "P", "انتشار"
        DRAFT = "D", "پیش نویس"

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='نویسنده')
    title = models.CharField(max_length=255, blank=False, verbose_name='تیتر')
    slug = models.SlugField(max_length=255, unique_for_date='published_at', verbose_name='اسلاگ', allow_unicode=True)
    category = models.ManyToManyField("Category", verbose_name='دسته بندی')
    content = models.TextField(verbose_name='محتوا')
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='وضعیت انتشار مقاله'
    )

    published_at = models.DateTimeField(default=timezone.now, verbose_name='منتشر شده در')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='بروزرسانی شده در')


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        args = [self.published_at.year,self.published_at.month,self.published_at.day,self.slug]
        return reverse('blog:post_detail',args=args)
    
    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
    
    


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام دسته بندی')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='مقاله')
    name = models.CharField(max_length=255, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    body = models.TextField(verbose_name='محتوا')
    active = models.BooleanField(default=True, verbose_name='وضعیت انتشار')
    created = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')
    updated = models.DateTimeField(auto_now=True, verbose_name='بروز رسانی شده در')

    class Meta:
        ordering = ['created',]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
    
    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"