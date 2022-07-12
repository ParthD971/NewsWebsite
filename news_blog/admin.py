from django.contrib import admin
from .models import (
    Categorie,
    PostStatus,
    Post,
    PostRecycle,
    NotificationType,
    PostNotification,
    NotificationStatus,
    ApplicationNotification,
    Follow,
    PostView,
    PCMiddle,
    PostStatusRecord
)
from users.constants import GROUP_EDITOR_NAME
from .filters import PostStatusFilter, FollowFilter, PostEditorFilter


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "views", "status")
    readonly_fields = ('views', 'author', 'created_on', 'post_type')
    list_filter = (PostStatusFilter, PostEditorFilter)
    search_fields = ('title', 'content')

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


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_filter = (FollowFilter,)


@admin.register(PostRecycle)
class FollowAdmin(admin.ModelAdmin):
    fields = ['post', 'deleted_by', 'recycle_created_on']
    readonly_fields = ['recycle_created_on']


admin.site.register(Categorie)
admin.site.register(PostView)
admin.site.register(NotificationType)
admin.site.register(PostStatus)
admin.site.register(PostNotification)
admin.site.register(NotificationStatus)
admin.site.register(ApplicationNotification)
admin.site.register(PCMiddle)
admin.site.register(PostStatusRecord)
admin.site.site_header = 'News Website Admin Panel'
