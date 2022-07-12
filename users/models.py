from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser


class UserType(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)

    # saves in lower-case
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.name.lower()
        super(UserType, self).save()

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, null=False)
    is_blocked = models.BooleanField(default=False)
    user_type = models.ForeignKey(UserType, on_delete=models.SET_DEFAULT, default=None, null=True)
    age = models.IntegerField(null=True)
    is_premium_user = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        group = self.groups.first()
        return group.name + ' | ' + self.first_name


class StripeCustomer(models.Model):
    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)

    def __str__(self):
        return self.user.first_name
