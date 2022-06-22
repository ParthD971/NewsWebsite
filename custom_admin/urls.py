from django.urls import path
from . import views


urlpatterns = [
    path('admin-panel/', views.AdminPanel.as_view(), name='admin_panel'),
    path('admin-panel/users-table/', views.UsersListView.as_view(), name='users_table'),
    path('admin-panel/users-table/change-user/<pk>/', views.UserUpdateView.as_view(), name='change_user'),


    path('admin-panel/application-table/', views.ApplicationNotificationListView.as_view(), name='application_notification_table'),
    path('admin-panel/application-table/change-application/<pk>/', views.ApplicationNotificationUpdateView.as_view(), name='change_application_notification'),

    path('manager-panel/', views.ManagerPanel.as_view(), name='manager_panel'),
    path('manager-panel/news-posts-table/', views.ManagersPostsListView.as_view(), name='managers_news_posts_table'),
    path('manager-panel/news-posts-table/change-news-post/<pk>/', views.ManagersPostUpdateView.as_view(), name='managers_change_news_post'),

    path('manager-panel/categories-table/', views.CategoryListView.as_view(), name='categories_table'),
    path('manager-panel/categories-table/add-category/', views.CategoryCreateView.as_view(), name='add_category'),
    path('manager-panel/categories-table/change-category/<pk>/', views.CategoryUpdateView.as_view(), name='change_category'),

    path('manager-panel/users-table/', views.ManagersUsersListView.as_view(), name='managers_users_table'),
    path('manager-panel/users-table/change-user/<pk>/', views.ManagersUserUpdateView.as_view(), name='managers_change_user'),

    path('editor-panel/', views.EditorPanel.as_view(), name='editor_panel'),
    path('editor-panel/news-posts-table/', views.EditorsPostsListView.as_view(), name='editors_news_posts_table'),
    path('editor-panel/news-posts-table/add-news-post/', views.PostsCreateView.as_view(), name='add_news_post'),
    path('editor-panel/news-posts-table/change-news-post/<pk>/', views.EditorsPostUpdateView.as_view(), name='editors_change_news_post'),


]
