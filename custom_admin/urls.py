from django.urls import path
from . import views


urlpatterns = [
    path('admin-panel/', views.AdminPanel.as_view(), name='admin_panel'),
    path('admin-panel/users-table/', views.UsersListView.as_view(), name='users_table'),
    path('admin-panel/users-table/change-user/<pk>/', views.UserUpdateView.as_view(), name='change_user'),
    path('admin-panel/categories/', views.AdminCategoriesListView.as_view(), name='admin_categories_listview'),
    path('admin-panel/follows/', views.AdminFollowsListView.as_view(), name='admin_follows_listview'),
    path('admin-panel/notification-status/', views.AdminNotificationStatusListView.as_view(), name='admin_notification_status_listview'),
    path('admin-panel/notification-types/', views.AdminNotificationTypeListView.as_view(), name='admin_notification_type_listview'),
    path('admin-panel/pcmiddles/', views.AdminPCMiddleListView.as_view(), name='admin_pcmiddle_listview'),
    path('admin-panel/post-notifications/', views.AdminPostNotificationListView.as_view(), name='admin_post_notification_listview'),
    path('admin-panel/post-recycles/', views.AdminPostRecycleListView.as_view(), name='admin_post_recycle_listview'),
    path('admin-panel/post-status-records/', views.AdminPostStatusRecordListView.as_view(), name='admin_post_status_records_listview'),
    path('admin-panel/post-status/', views.AdminPostStatusListView.as_view(), name='admin_post_status_listview'),
    path('admin-panel/post-views/', views.AdminPostViewsListView.as_view(), name='admin_post_view_listview'),
    path('admin-panel/posts/', views.AdminPostsListView.as_view(), name='admin_posts_listview'),
    path('admin-panel/user-types/', views.AdminUserTypeListView.as_view(), name='admin_user_type_listview'),
    path('admin-panel/manager-comments/', views.AdminManagerCommentsListView.as_view(), name='admin_manager_comments_listview'),
    path('admin-panel/admin-notifications/', views.AdminNotificationListView.as_view(), name='admin_notification_listview'),

    path('admin-panel/send-notification/', views.AdminSendNotificationView.as_view(), name='send-notification'),



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

    path('manager-panel/restore_posts/', views.ManagersRestorePostListView.as_view(), name='managers_restore_post_table'),
    path('manager-panel/restore_posts/<pk>/', views.RestoreManagersNewsConfirmView.as_view(), name='managers_restore_news_post'),

    path('editor-panel/', views.EditorPanel.as_view(), name='editor_panel'),
    path('editor-panel/news-posts-table/', views.EditorsPostsListView.as_view(), name='editors_news_posts_table'),
    path('editor-panel/news-posts-table/add-news-post/', views.PostsCreateView.as_view(), name='add_news_post'),
    path('editor-panel/news-posts-table/change-news-post/<pk>/', views.EditorsPostUpdateView.as_view(), name='editors_change_news_post'),
    path('editor-panel/news-posts-table/delete-news-post/<pk>/', views.EditorsPostDeleteView.as_view(), name='editors_delete_news_post'),
    path('editor-panel/restore_posts/', views.EditorsRestorePostListView.as_view(), name='editors_restore_post_table'),
    path('editor-panel/restore_posts/<pk>/', views.RestoreEditorsNewsConfirmView.as_view(), name='editors_restore_news_post'),


    path('manager-panel/news-posts-table/comment/<pk>/', views.ManagersAddCommentView.as_view(), name='add_comment_to_post'),
    path('editor-panel/news-posts-table/comment/<pk>/', views.EditorsCommentListView.as_view(), name='editors_comments_list'),

]
