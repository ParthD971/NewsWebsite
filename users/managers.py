from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import users.models as users_model
from django.contrib.auth.models import Group


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        try:
            admin_type = users_model.UserType.objects.get(name='admin')
        except users_model.UserType.DoesNotExist as e:
            raise ValueError(_('User Type \'admin\' does not exists.'))

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', admin_type)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        super_user = self.create_user(email, password, **extra_fields)

        try:
            my_group = Group.objects.get(name='admin')
            my_group.user_set.add(super_user)
        except Group.DoesNotExist as e:
            super_user.delete()
            raise ValueError(_('Group \'admin\' does not exists.'))

        return super_user
