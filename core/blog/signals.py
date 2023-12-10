from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Post

@receiver(signal=pre_save, sender=Post)
def creat_auto_post_slug(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title, allow_unicode=True)