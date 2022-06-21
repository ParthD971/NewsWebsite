from django.urls import path
from . import views


urlpatterns = [
    path('', views.AdminPanel.as_view(), name='admin_panel'),
    path('users-table/', views.UsersListView.as_view(), name='users_table'),
    path('users-table/change-user/<pk>/', views.UserUpdateView.as_view(), name='change_user'),
    path('users-table/delete-user/<pk>/', views.UserDeleteView.as_view(), name='delete_user'),
]