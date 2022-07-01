from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from news_blog import views as news_blog_views

urlpatterns = [
    path('admin/', admin.site.urls, name='django-admin'),
    path('scrap/', news_blog_views.RunScrapper.as_view(), name='run-scraper'),
    path('cadmin/', include('custom_admin.urls')),
    path('user/', include('users.urls')),
    path('', include('news_blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



