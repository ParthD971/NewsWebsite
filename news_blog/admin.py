from django.contrib import admin
from .models import Categorie, Post, Notification, Follow
from django import forms


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('author', 'views', )

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            group_name = request.user.groups.first().name
            if group_name == 'Editor':
                form.base_fields['status'].disabled = True

        return form

    def save_model(self, request, obj, form, change):
        try:
            obj.author = request.user
            obj.save()
        except Exception as e:
            print(str(e))


# Register your models here.
admin.site.register(Categorie)
# admin.site.register(Post)
admin.site.register(Notification)
admin.site.register(Follow)