from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from .constants import GROUP_EDITOR_NAME
from .models import PostStatus
from django.contrib.auth.models import Group


class PostStatusFilter(SimpleListFilter):
    title = _('Post Status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('is_active', 'Active'),
            ('is_pending', 'Pending'),
            ('is_inactive', 'Inactive')
        )

    def queryset(self, request, queryset):
        if self.value() == 'is_active':
            status = PostStatus.objects.get('active')
            return queryset.filter(status=status)
        elif self.value() == 'is_pending':
            status = PostStatus.objects.get('pending')
            return queryset.filter(status=status)
        elif self.value() == 'is_inactive':
            status = PostStatus.objects.get('inactive')
            return queryset.filter(status=status)
        return queryset


class PostEditorFilter(SimpleListFilter):
    title = _('Post Editor')
    parameter_name = 'editor'

    def lookups(self, request, model_admin):
        users = Group.objects.get(name=GROUP_EDITOR_NAME).user_set.all()
        result = tuple([(user.email, user.first_name) for user in users])
        return result

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(author__email=self.value())
        return queryset


class FollowFilter(SimpleListFilter):
    title = _('Editors')
    parameter_name = 'editor'

    def lookups(self, request, model_admin):
        users = Group.objects.get(name=GROUP_EDITOR_NAME).user_set.all()
        result = tuple([(user.email, user.first_name) for user in users])
        return result

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(author__email=self.value())
        return queryset
