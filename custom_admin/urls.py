from django.urls import path
from . import views


urlpatterns = [
    path('', views.AdminPanel.as_view(), name='admin_panel'),
    path('users-table/', views.UsersListView.as_view(), name='users_table'),
    path('users-table/change-user/<pk>/', views.UserUpdateView.as_view(), name='change_user'),


    path('application-table/', views.ApplicationNotificationListView.as_view(), name='application_notification_table'),
    path('application-table/change-application/<pk>/', views.ApplicationNotificationUpdateView.as_view(), name='change_application_notification'),
]