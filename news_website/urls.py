from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from news_blog import views as news_blog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('custom-admin/', include('custom_admin.urls')),
    path('user/', include('users.urls')),
    path('scrap/', news_blog_views.run_scraper, name='run_scraper'),
    path('', include('news_blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



