from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Post

@receiver(signal=pre_save, sender=Post)
def creat_auto_post_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = creat_uniq_slug(instance)



def creat_uniq_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title, allow_unicode=True)
    
    # instance.__class__ its same Post
    qs = instance.__class__.objects.filter(slug=slug)

    if qs.exists():
        new_slug = f"{slug}-{qs.first().id}"
        return creat_uniq_slug(instance, new_slug)
    
    return slug


