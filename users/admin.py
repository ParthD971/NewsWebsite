from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, UserType, StripeCustomer
from .filters import UserBlockedFilter, UserTypeFilter


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = (UserBlockedFilter, UserTypeFilter, 'is_staff', 'is_active', 'is_premium_user')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_blocked', 'user_type', 'is_premium_user')}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ('Permissions', {'fields': ('is_staff', 'is_active', "is_superuser", "groups",)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        print(request.user.is_superuser)
        if not request.user.is_superuser:
            print('>>>>>')
            self.fieldsets = (
                (None, {'fields': ('email', 'password', 'is_blocked')}),
                ("Personal info", {"fields": ("first_name", "last_name")}),
                ('Permissions', {'fields': ('is_staff', 'is_active', "is_superuser", "groups",)}),
            )
            self.readonly_fields = (
                'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups'
            )
        form = super().get_form(request, obj, **kwargs)
        return form


admin.site.register(UserType)
admin.site.register(StripeCustomer)
