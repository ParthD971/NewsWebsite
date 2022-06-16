from django.db import models
from users.models import CustomUser as User
from .constants import POST_STATUS_CHOICES, POST_TYPE_CHOICES


class Categorie(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.name.lower()
        super(Categorie, self).save()

    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=5, choices=POST_STATUS_CHOICES, default='PEN')
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images/', default='default.jpg')
    type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='MANUAL')

    def __str__(self):
        return ' | '.join([str(self.author), str(self.title), str(self.category), str(self.status)])


class Notification(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Follow(models.Model):
    author_id = models.ForeignKey(User, related_name='editor', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)