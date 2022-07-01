from django.urls import path
from . import admin_views, manager_views, editor_views


urlpatterns = [
    path('admin-panel/', admin_views.AdminMainPageView.as_view(), name='admin-panel'),
    path('admin-panel/users/', admin_views.AdminUserListView.as_view(), name='admin-user-list'),
    path('admin-panel/users/change/<pk>/', admin_views.AdminUserUpdateView.as_view(), name='admin-user-update'),
    path('admin-panel/categories/', admin_views.AdminCategorieListView.as_view(), name='admin-categorie-list'),
    path('admin-panel/follows/', admin_views.AdminFollowListView.as_view(), name='admin-follow-list'),
    path('admin-panel/notification-statuses/', admin_views.AdminNotificationStatusListView.as_view(), name='admin-notification-status-list'),
    path('admin-panel/notification-types/', admin_views.AdminNotificationTypeListView.as_view(), name='admin-notification-type-list'),
    path('admin-panel/pcmiddles/', admin_views.AdminPCMiddleListView.as_view(), name='admin-pcmiddle-list'),
    path('admin-panel/post-notifications/', admin_views.AdminPostNotificationListView.as_view(), name='admin-post-notification-list'),
    path('admin-panel/post-recycles/', admin_views.AdminPostRecycleListView.as_view(), name='admin-post-recycle-list'),
    path('admin-panel/post-status-records/', admin_views.AdminPostStatusRecordListView.as_view(), name='admin-post-status-record-list'),
    path('admin-panel/post-statuses/', admin_views.AdminPostStatusListView.as_view(), name='admin-post-status-list'),
    path('admin-panel/post-views/', admin_views.AdminPostViewsListView.as_view(), name='admin-post-view-list'),
    path('admin-panel/posts/', admin_views.AdminPostListView.as_view(), name='admin-post-list'),
    path('admin-panel/user-types/', admin_views.AdminUserTypeListView.as_view(), name='admin-user-type-list'),
    path('admin-panel/manager-comments/', admin_views.AdminManagerCommentListView.as_view(), name='admin-manager-comment-list'),
    path('admin-panel/admin-notifications/', admin_views.AdminNotificationListView.as_view(), name='admin-notification-list'),
    path('admin-panel/send-notification/', admin_views.AdminSendNotificationView.as_view(), name='admin-send-notification'),
    path('admin-panel/admin-application/', admin_views.AdminApplicationNotificationListView.as_view(), name='admin-application-notification-list'),
    path('admin-panel/admin-application/change/<pk>/', admin_views.AdminApplicationNotificationUpdateView.as_view(), name='admin-application-notification-update'),

    path('manager-panel/', manager_views.ManagerMainPageView.as_view(), name='manager-panel'),
    path('manager-panel/posts/', manager_views.ManagerPostListView.as_view(), name='manager-post-list'),
    path('manager-panel/posts/change/<pk>/', manager_views.ManagerPostUpdateView.as_view(), name='manager-post-update'),
    path('manager-panel/categories/', manager_views.ManagerCategorieListView.as_view(), name='manager-categorie-list'),
    path('manager-panel/categories/add/', manager_views.ManagerCategorieCreateView.as_view(), name='manager-categorie-create'),
    path('manager-panel/categories/change/<pk>/', manager_views.ManagerCategorieUpdateView.as_view(), name='manager-categorie-update'),
    path('manager-panel/users/', manager_views.ManagerUserListView.as_view(), name='manager-user-list'),
    path('manager-panel/users/change/<pk>/', manager_views.ManagerUserUpdateView.as_view(), name='manager-user-update'),
    path('manager-panel/restore_posts/', manager_views.ManagerRestorePostListView.as_view(), name='manager-restore-post-list'),
    path('manager-panel/restore_post/<pk>/', manager_views.ManagerRestorePostConfirmView.as_view(), name='manager-restore-post'),
    path('manager-panel/posts/comment/<pk>/', manager_views.ManagerAddCommentView.as_view(), name='manager-add-comment'),

    path('editor-panel/', editor_views.EditorMainPageView.as_view(), name='editor-panel'),
    path('editor-panel/posts/', editor_views.EditorPostListView.as_view(), name='editor-post-list'),
    path('editor-panel/posts/add/', editor_views.EditorPostCreateView.as_view(), name='editor-post-create'),
    path('editor-panel/posts-table/change/<pk>/', editor_views.EditorPostUpdateView.as_view(), name='editor-post-update'),
    path('editor-panel/posts-table/delete/<pk>/', editor_views.EditorPostDeleteView.as_view(), name='editor-post-delete'),
    path('editor-panel/restore_posts/', editor_views.EditorRestorePostListView.as_view(), name='editor-restore-post-list'),
    path('editor-panel/restore_post/<pk>/', editor_views.EditorRestorePostConfirmView.as_view(), name='editor-restore-post-confirm'),
    path('editor-panel/posts/comment/<pk>/', editor_views.EditorCommentListView.as_view(), name='editor-comment-list'),

]
