from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Post
from uuid import uuid4
@receiver(signal=pre_save, sender=Post)
def creat_auto_post_slug(sender, instance, *args, **kwargs):
    title = slugify(instance.title, allow_unicode=True)
    uuid = str(uuid4())[:8]
    instance.slug = f"{title}-l{uuid}"
