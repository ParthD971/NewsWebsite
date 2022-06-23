from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('news-post/<pk>/', views.PostDetailView.as_view(), name='news_detail'),
    path('author/', views.PostAuthorListView.as_view(), name='author_news_list'),
    path('manager-application/', views.ManagerApplicationView.as_view(), name='apply_for_manager'),
    path('editor-application/', views.EditorApplicationView.as_view(), name='apply_for_editor'),
]
