from django.db import models
from users.models import CustomUser as User
from news_blog.models import Post


class ManagerComment(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    comment = models.TextField()

    def __str__(self):
        return ' | '.join([self.manager.first_name, self.post.title])