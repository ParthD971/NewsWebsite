from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from news_blog.constants import GROUP_EDITOR_NAME, GROUP_MANAGER_NAME, GROUP_CONSUMER_NAME


class UserBlockedFilter(SimpleListFilter):
    title = _('User Blocked')
    parameter_name = 'blocked'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Blocked'),
            ('0', 'Un-Blocked'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(is_blocked=True)
        elif self.value() == '0':
            return queryset.filter(is_blocked=False)
        return queryset


class UserTypeFilter(SimpleListFilter):
    title = _('User Type')
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        return (
            ('admin', 'Admin'),
            ('manager', 'Manager'),
            ('editor', 'Editor'),
            ('consumer', 'Consumer'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'admin':
            return queryset.filter(is_superuser=True)
        elif self.value() == 'manager':
            return queryset.filter(groups__name=GROUP_MANAGER_NAME)
        elif self.value() == 'editor':
            return queryset.filter(groups__name=GROUP_EDITOR_NAME)
        elif self.value() == 'consumer':
            return queryset.filter(groups__name=GROUP_CONSUMER_NAME)
        return queryset


