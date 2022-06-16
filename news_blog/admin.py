from django.contrib import admin
from .models import Categorie, Post, Notification, Follow
from .constants import GROUP_EDITOR_NAME

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # list_display = ("author", "title", "views", "status")
    readonly_fields = ('views', 'author', 'created_on', 'type')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            group_name = request.user.groups.first().name
            if group_name == GROUP_EDITOR_NAME:
                form.base_fields['status'].disabled = True
        return form


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()
        if not request.user.is_superuser:
            group_name = request.user.groups.first().name
            if group_name == GROUP_EDITOR_NAME:
                queryset = queryset.filter(author_id=request.user.id, status='PEN')
        return queryset

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
            obj.save()
        else:
            obj.save()


# Register your models here.
admin.site.register(Categorie)
admin.site.register(Notification)
admin.site.register(Follow)