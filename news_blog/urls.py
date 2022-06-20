from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('manager-application/', views.ManagerApplicationView.as_view(), name='apply_for_manager'),
    path('editor-application/', views.HomeView.as_view(), name='apply_for_editor'),
]
