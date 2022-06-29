from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('news-post/<pk>/', views.PostDetailView.as_view(), name='news_detail'),
    path('follow/<pk>/', views.FollowView.as_view(), name='follow'),
    path('notification-seen/', views.NotificationSeenView.as_view(), name='notification_seen'),
    path('notifications/', views.PostNotificationListView.as_view(), name='notification_list'),
    path('add_views/', views.AddViewsView.as_view(), name='add_views'),
    path('manager-application/', views.ManagerApplicationView.as_view(), name='apply_for_manager'),
    path('editor-application/', views.EditorApplicationView.as_view(), name='apply_for_editor'),
    path('premium-user-application/', views.PremiumApplyView.as_view(), name='apply_for_premium_user'),
]




