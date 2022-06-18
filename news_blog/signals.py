from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from news_blog.models import Post, Notification, Follow
from news_blog.constants import DEFAULT_IMAGE_NAME, POST_STATUS_CHOICES


@receiver(pre_delete, sender=Post)
def delete_post_image(sender, instance, **kwargs):
    if instance.image and instance.image.url.split('/')[-1] != DEFAULT_IMAGE_NAME:
        instance.image.delete(False)


@receiver(post_save, sender=Post)
def send_notification(sender, instance, **kwargs):
    # active status
    if instance.status == POST_STATUS_CHOICES[1][0]:
        followers = Follow.objects.select_related('user').filter(author=instance.author)
        notifications = [Notification(post=instance, user=follower.user) for follower in followers]
        Notification.objects.bulk_create(notifications)

    # inactive status
    elif instance.status == POST_STATUS_CHOICES[2][0]:
        followers = Follow.objects.filter(author=instance.author).values_list('user')
        followers = [_[0] for _ in followers]
        Notification.objects.filter(post=instance, user_id__in=followers).delete()





