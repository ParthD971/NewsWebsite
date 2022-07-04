from django.db import models
from users.models import CustomUser as User
from .constants import POST_TYPE_CHOICES, POST_IMAGE_UPLOAD_TO, DEFAULT_IMAGE_PATH
from django.utils import timezone


class Categorie(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    description = models.CharField(max_length=200, blank=False, null=True)

    # saves in lower-case
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.name.lower()
        super(Categorie, self).save()

    def __str__(self):
        return self.name


class PostStatus(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=False, null=False)

    # saves in lower-case
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.name.lower()
        super(PostStatus, self).save()

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)
    content = models.TextField(blank=False, null=False)
    created_on = models.DateField(default=timezone.now)
    views = models.IntegerField(default=0, blank=False, null=False)
    status = models.ForeignKey(PostStatus, on_delete=models.CASCADE, null=False)
    category = models.ManyToManyField(Categorie, through='PCMiddle')
    image = models.ImageField(upload_to=POST_IMAGE_UPLOAD_TO, default=DEFAULT_IMAGE_PATH)
    # Type : SCRAPED or MANUAL
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default=POST_TYPE_CHOICES[1][0])
    author_display_name = models.CharField(max_length=50, default=None, null=True)
    premium = models.BooleanField(default=False)
    
    def __str__(self):
        return ' | '.join([str(self.author), str(self.title), str(self.category), str(self.status)])


class PCMiddle(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)


class PostRecycle(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    recycle_created_on = models.DateField(default=timezone.now)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.post.title


class NotificationType(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)

    # saves in lower-case
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.name.lower()
        super(NotificationType, self).save()

    def __str__(self):
        return self.name


class PostNotification(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    # User : Person who will receive notification
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    seen = models.BooleanField(default=False)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return ' -> '.join([str(self.post), self.user.first_name])


class NotificationStatus(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=False, null=False)

    # saves in lower-case
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.name.lower()
        super(NotificationStatus, self).save()

    def __str__(self):
        return self.name


class ApplicationNotification(models.Model):
    # User : Person who will send notification
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE, null=False)
    status = models.ForeignKey(NotificationStatus, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return ' | '.join([self.user.first_name, self.status.name, self.notification_type.name])


class Follow(models.Model):
    author = models.ForeignKey(User, related_name='editor', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name='consumer', on_delete=models.CASCADE, null=False)
    author_name = models.CharField(max_length=50, default=None, null=True)



class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    viewed_on = models.DateField(default=timezone.now)


class PostStatusRecord(models.Model):
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    status = models.ForeignKey(PostStatus, on_delete=models.CASCADE, null=False)
    changed_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return ' | '.join([self.changed_by.first_name, self.status.name])

