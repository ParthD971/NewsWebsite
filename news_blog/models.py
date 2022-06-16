from django.db import models
from users.models import CustomUser as User
from .constants import POST_STATUS_CHOICES, POST_TYPE_CHOICES, DEFAULT_IMAGE_NAME, POST_IMAGE_UPLOAD_TO, DEFAULT_IMAGE_PATH
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Categorie(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.name.lower()
        super(Categorie, self).save()

    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    content = models.TextField()
    created_on = models.DateField(auto_now_add=True, blank=False, null=False)
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=5, choices=POST_STATUS_CHOICES, default=POST_STATUS_CHOICES[0][0])
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE, blank=False, null=False)
    image = models.ImageField(upload_to=POST_IMAGE_UPLOAD_TO, default=DEFAULT_IMAGE_PATH)
    type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default=POST_TYPE_CHOICES[1][0])

    def __str__(self):
        # return ' | '.join([str(self.author), str(self.title), str(self.category), str(self.status)])
        return self.image.url

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        img = Image.open(self.image)
        output = BytesIO()
        if any([img.width > settings.MAX_PROFILE_PICTURE_WIDTH, img.height > settings.MAX_PROFILE_PICTURE_HEIGHT]):
            img.thumbnail(settings.MAX_PROFILE_PICTURE_DIMENSIONS, Image.ANTIALIAS)
            img.save(output, format='JPEG', quality=100)
            output.seek(0)
            self.image = InMemoryUploadedFile(
                output,
                'ImageField',
                "%s.jpg" % self.image.name.split('.')[0],
                'image/jpeg',
                sys.getsizeof(output),
                None
            )
        super().save()


class Notification(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Follow(models.Model):
    author_id = models.ForeignKey(User, related_name='editor', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)