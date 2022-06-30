from django.contrib import admin
from .models import ManagerComment, AdminNotification

# Register your models here.
admin.site.register(ManagerComment)
admin.site.register(AdminNotification)