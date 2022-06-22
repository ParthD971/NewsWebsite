from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('custom-admin/', include('custom_admin.urls')),
    path('user/', include('users.urls')),
    path('', include('news_blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
