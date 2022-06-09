from django.contrib import admin
from .models import Categorie, Post, Notification, Follow

# Register your models here.
admin.site.register(Categorie)
admin.site.register(Post)
admin.site.register(Notification)
admin.site.register(Follow)