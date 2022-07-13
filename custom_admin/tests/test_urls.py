from django.urls import reverse, resolve
from custom_admin.views.admin_views import (
    AdminMainPageView, AdminUserListView, AdminUserUpdateView, AdminCategorieListView, AdminFollowListView,
    AdminNotificationStatusListView, AdminNotificationTypeListView, AdminPCMiddleListView,
    AdminPostNotificationListView, AdminPostRecycleListView, AdminPostStatusRecordListView, AdminPostStatusListView,
    AdminPostViewsListView, AdminPostListView, AdminUserTypeListView, AdminManagerCommentListView,
    AdminNotificationListView, AdminSendNotificationView, AdminApplicationNotificationListView,
    AdminApplicationNotificationUpdateView
)
from custom_admin.views.editor_views import (
    EditorMainPageView, EditorPostListView, EditorPostCreateView, EditorPostUpdateView, EditorPostDeleteView,
    EditorRestorePostListView, EditorRestorePostConfirmView, EditorCommentListView
)
from custom_admin.views.manager_views import (
    ManagerMainPageView, ManagerPostListView, ManagerPostUpdateView, ManagerCategorieListView,
    ManagerCategorieCreateView, ManagerCategorieUpdateView, ManagerUserListView, ManagerUserUpdateView,
    ManagerRestorePostListView, ManagerRestorePostConfirmView, ManagerAddCommentView
)


class TestAdminPanelUrls(object):
    """Test Class for Custom Admin app's (admin-panel) urls.
    Below test functions tests for all urls defined in custom_admin/urls.py
    """

    # PK for admin-user-update and admin-application-notification-update
    pk = 1

    def test_admin_panel_url(self):
        url = reverse('admin-panel')
        assert resolve(url).func.__name__ == AdminMainPageView.as_view().__name__

    def test_admin_user_list_url(self):
        url = reverse('admin-user-list')
        assert resolve(url).func.__name__ == AdminUserListView.as_view().__name__

    def test_admin_user_update_url(self):
        url = reverse('admin-user-update', kwargs={'pk': self.pk})
        assert resolve(url).func.__name__ == AdminUserUpdateView.as_view().__name__

    def test_admin_categorie_list_url(self):
        url = reverse('admin-categorie-list')
        assert resolve(url).func.__name__ == AdminCategorieListView.as_view().__name__

    def test_admin_follow_list_url(self):
        url = reverse('admin-follow-list')
        assert resolve(url).func.__name__ == AdminFollowListView.as_view().__name__

    def test_admin_notification_status_list_url(self):
        url = reverse('admin-notification-status-list')
        assert resolve(url).func.__name__ == AdminNotificationStatusListView.as_view().__name__

    def test_admin_notification_type_list_url(self):
        url = reverse('admin-notification-type-list')
        assert resolve(url).func.__name__ == AdminNotificationTypeListView.as_view().__name__

    def test_admin_pcmiddle_list_url(self):
        url = reverse('admin-pcmiddle-list')
        assert resolve(url).func.__name__ == AdminPCMiddleListView.as_view().__name__

    def test_admin_post_notification_list_url(self):
        url = reverse('admin-post-notification-list')
        assert resolve(url).func.__name__ == AdminPostNotificationListView.as_view().__name__

    def test_admin_post_recycle_list_url(self):
        url = reverse('admin-post-recycle-list')
        assert resolve(url).func.__name__ == AdminPostRecycleListView.as_view().__name__

    def test_admin_post_status_record_list_url(self):
        url = reverse('admin-post-status-record-list')
        assert resolve(url).func.__name__ == AdminPostStatusRecordListView.as_view().__name__

    def test_admin_post_status_list_url(self):
        url = reverse('admin-post-status-list')
        assert resolve(url).func.__name__ == AdminPostStatusListView.as_view().__name__

    def test_admin_post_view_list_url(self):
        url = reverse('admin-post-view-list')
        assert resolve(url).func.__name__ == AdminPostViewsListView.as_view().__name__

    def test_admin_post_list_url(self):
        url = reverse('admin-post-list')
        assert resolve(url).func.__name__ == AdminPostListView.as_view().__name__

    def test_admin_user_type_list_url(self):
        url = reverse('admin-user-type-list')
        assert resolve(url).func.__name__ == AdminUserTypeListView.as_view().__name__

    def test_admin_manager_comment_list_url(self):
        url = reverse('admin-manager-comment-list')
        assert resolve(url).func.__name__ == AdminManagerCommentListView.as_view().__name__

    def test_admin_notification_list_url(self):
        url = reverse('admin-notification-list')
        assert resolve(url).func.__name__ == AdminNotificationListView.as_view().__name__

    def test_admin_send_notification_url(self):
        url = reverse('admin-send-notification')
        assert resolve(url).func.__name__ == AdminSendNotificationView.as_view().__name__

    def test_admin_application_notification_list_url(self):
        url = reverse('admin-application-notification-list')
        assert resolve(url).func.__name__ == AdminApplicationNotificationListView.as_view().__name__

    def test_admin_application_notification_update_url(self):
        url = reverse('admin-application-notification-update', kwargs={'pk': self.pk})
        assert resolve(url).func.__name__ == AdminApplicationNotificationUpdateView.as_view().__name__


class TestManagerPanelUrls(object):
    """Test Class for Custom Admin app's (manager-panel) urls.
    Below test functions tests for all urls defined in custom_admin/urls.py
    """

    # PK for manager-post-update, manager-categorie-update, manager-user-update
    # manager-restore-post and manager-add-comment
    pk = 1

    def test_manager_panel_url(self):
        url = reverse('manager-panel')
        assert resolve(url).func.__name__ == ManagerMainPageView.as_view().__name__

    def test_manager_post_list_url(self):
        url = reverse('manager-post-list')
        assert resolve(url).func.__name__ == ManagerPostListView.as_view().__name__

    def test_manager_post_update_url(self):
        url = reverse('manager-post-update', kwargs={'pk': self.pk})
        assert resolve(url).func.__name__ == ManagerPostUpdateView.as_view().__name__

    def test_manager_categorie_list_url(self):
        url = reverse('manager-categorie-list')
        assert resolve(url).func.__name__ == ManagerCategorieListView.as_view().__name__

    def test_manager_categorie_create_url(self):
        url = reverse('manager-categorie-create')
        assert resolve(url).func.__name__ == ManagerCategorieCreateView.as_view().__name__

    def test_manager_categorie_update_url(self):
        url = reverse('manager-categorie-update', kwargs={'pk': self.pk})
        assert resolve(url).func.__name__ == ManagerCategorieUpdateView.as_view().__name__

    def test_manager_user_list_url(self):
        url = reverse('manager-user-list')
        assert resolve(url).func.__name__ == ManagerUserListView.as_view().__name__

    def test_manager_user_update_url(self):
        url = reverse('manager-user-update', kwargs={'pk': self.pk})
        assert resolve(url).func.__name__ == ManagerUserUpdateView.as_view().__name__

    def test_manager_restore_post_list_url(self):
        url = reverse('manager-restore-post-list')
        assert resolve(url).func.__name__ == ManagerRestorePostListView.as_view().__name__

    def test_manager_restore_post_url(self):
        url = reverse('manager-restore-post', kwargs={'pk': self.pk})
        assert resolve(url).func.__name__ == ManagerRestorePostConfirmView.as_view().__name__

    def test_manager_add_comment_url(self):
        url = reverse('manager-add-comment', kwargs={'pk': self.pk})
        assert resolve(url).func.__name__ == ManagerAddCommentView.as_view().__name__


class TestEditorPanelUrls(object):
    """Test Class for Custom Admin app's (editor-panel) urls.
    Below test functions tests for all urls defined in custom_admin/urls.py
    """

    # PK for editor-post-update, editor-post-delete, editor-restore-post-confirm and editor-comment-list
    pk = 1

    def test_editor_panel_url(self):
        url = reverse('editor-panel')
        assert resolve(url).func.__name__ == EditorMainPageView.as_view().__name__

    def test_editor_post_list_url(self):
        url = reverse('editor-post-list')
        assert resolve(url).func.__name__ == EditorPostListView.as_view().__name__

    def test_editor_post_create_url(self):
        url = reverse('editor-post-create')
        assert resolve(url).func.__name__ == EditorPostCreateView.as_view().__name__

    def test_editor_post_update_url(self):
        url = reverse('editor-post-update', kwargs={'pk': self.pk})
        assert resolve(url).func.__name__ == EditorPostUpdateView.as_view().__name__

    def test_editor_post_delete_url(self):
        url = reverse('editor-post-delete', kwargs={'pk': self.pk})
        assert resolve(url).func.__name__ == EditorPostDeleteView.as_view().__name__

    def test_editor_restore_post_list_url(self):
        url = reverse('editor-restore-post-list')
        assert resolve(url).func.__name__ == EditorRestorePostListView.as_view().__name__

    def test_editor_restore_post_confirm_url(self):
        url = reverse('editor-restore-post-confirm', kwargs={'pk': self.pk})
        assert resolve(url).func.__name__ == EditorRestorePostConfirmView.as_view().__name__

    def test_editor_comment_list_url(self):
        url = reverse('editor-comment-list', kwargs={'pk': self.pk})
        assert resolve(url).func.__name__ == EditorCommentListView.as_view().__name__
