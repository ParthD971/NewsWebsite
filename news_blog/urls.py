from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('follow/<pk>/', views.FollowView.as_view(), name='follow'),
    path('notification-seen/', views.NotificationSeenView.as_view(), name='notification-seen'),
    path('notifications/', views.PostNotificationListView.as_view(), name='notification-list'),
    path('add-views/', views.AddViewsView.as_view(), name='add-views'),
    path('application-for-manager/', views.ManagerApplicationView.as_view(), name='apply-for-manager'),
    path('application-for-editor/', views.EditorApplicationView.as_view(), name='apply-for-editor'),
    path('application-for-premium-user/', views.PremiumApplyView.as_view(), name='apply-for-premium-user'),
    path('notification-from-admin/', views.NotificationFromAdminView.as_view(), name='notification-from-admin'),
    path('notification-from-admin-seen/', views.NotificationFromAdminSeenView.as_view(), name='admin-notification-seen'),
]




