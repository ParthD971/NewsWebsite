from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from news_blog.models import Post
from news_blog.constants import DEFAULT_IMAGE_NAME


@receiver(pre_delete, sender=Post)
def delete_post_image(sender, instance, **kwargs):
    if instance.image and instance.image.url.split('/')[-1] != DEFAULT_IMAGE_NAME:
        instance.image.delete(False)








