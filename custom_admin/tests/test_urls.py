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
        assert resolve(url).func.view_class == AdminMainPageView

    def test_admin_user_list_url(self):
        url = reverse('admin-user-list')
        assert resolve(url).func.view_class == AdminUserListView

    def test_admin_user_update_url(self):
        url = reverse('admin-user-update', kwargs={'pk': self.pk})
        assert resolve(url).func.view_class == AdminUserUpdateView

    def test_admin_categorie_list_url(self):
        url = reverse('admin-categorie-list')
        assert resolve(url).func.view_class == AdminCategorieListView

    def test_admin_follow_list_url(self):
        url = reverse('admin-follow-list')
        assert resolve(url).func.view_class == AdminFollowListView

    def test_admin_notification_status_list_url(self):
        url = reverse('admin-notification-status-list')
        assert resolve(url).func.view_class == AdminNotificationStatusListView

    def test_admin_notification_type_list_url(self):
        url = reverse('admin-notification-type-list')
        assert resolve(url).func.view_class == AdminNotificationTypeListView

    def test_admin_pcmiddle_list_url(self):
        url = reverse('admin-pcmiddle-list')
        assert resolve(url).func.view_class == AdminPCMiddleListView

    def test_admin_post_notification_list_url(self):
        url = reverse('admin-post-notification-list')
        assert resolve(url).func.view_class == AdminPostNotificationListView

    def test_admin_post_recycle_list_url(self):
        url = reverse('admin-post-recycle-list')
        assert resolve(url).func.view_class == AdminPostRecycleListView

    def test_admin_post_status_record_list_url(self):
        url = reverse('admin-post-status-record-list')
        assert resolve(url).func.view_class == AdminPostStatusRecordListView

    def test_admin_post_status_list_url(self):
        url = reverse('admin-post-status-list')
        assert resolve(url).func.view_class == AdminPostStatusListView

    def test_admin_post_view_list_url(self):
        url = reverse('admin-post-view-list')
        assert resolve(url).func.view_class == AdminPostViewsListView

    def test_admin_post_list_url(self):
        url = reverse('admin-post-list')
        assert resolve(url).func.view_class == AdminPostListView

    def test_admin_user_type_list_url(self):
        url = reverse('admin-user-type-list')
        assert resolve(url).func.view_class == AdminUserTypeListView

    def test_admin_manager_comment_list_url(self):
        url = reverse('admin-manager-comment-list')
        assert resolve(url).func.view_class == AdminManagerCommentListView

    def test_admin_notification_list_url(self):
        url = reverse('admin-notification-list')
        assert resolve(url).func.view_class == AdminNotificationListView

    def test_admin_send_notification_url(self):
        url = reverse('admin-send-notification')
        assert resolve(url).func.view_class == AdminSendNotificationView

    def test_admin_application_notification_list_url(self):
        url = reverse('admin-application-notification-list')
        assert resolve(url).func.view_class == AdminApplicationNotificationListView

    def test_admin_application_notification_update_url(self):
        url = reverse('admin-application-notification-update', kwargs={'pk': self.pk})
        assert resolve(url).func.view_class == AdminApplicationNotificationUpdateView


class TestManagerPanelUrls(object):
    """Test Class for Custom Admin app's (manager-panel) urls.
    Below test functions tests for all urls defined in custom_admin/urls.py
    """

    # PK for manager-post-update, manager-categorie-update, manager-user-update
    # manager-restore-post and manager-add-comment
    pk = 1

    def test_manager_panel_url(self):
        url = reverse('manager-panel')
        assert resolve(url).func.view_class == ManagerMainPageView

    def test_manager_post_list_url(self):
        url = reverse('manager-post-list')
        assert resolve(url).func.view_class == ManagerPostListView

    def test_manager_post_update_url(self):
        url = reverse('manager-post-update', kwargs={'pk': self.pk})
        assert resolve(url).func.view_class == ManagerPostUpdateView

    def test_manager_categorie_list_url(self):
        url = reverse('manager-categorie-list')
        assert resolve(url).func.view_class == ManagerCategorieListView

    def test_manager_categorie_create_url(self):
        url = reverse('manager-categorie-create')
        assert resolve(url).func.view_class == ManagerCategorieCreateView

    def test_manager_categorie_update_url(self):
        url = reverse('manager-categorie-update', kwargs={'pk': self.pk})
        assert resolve(url).func.view_class == ManagerCategorieUpdateView

    def test_manager_user_list_url(self):
        url = reverse('manager-user-list')
        assert resolve(url).func.view_class == ManagerUserListView

    def test_manager_user_update_url(self):
        url = reverse('manager-user-update', kwargs={'pk': self.pk})
        assert resolve(url).func.view_class == ManagerUserUpdateView

    def test_manager_restore_post_list_url(self):
        url = reverse('manager-restore-post-list')
        assert resolve(url).func.view_class == ManagerRestorePostListView

    def test_manager_restore_post_url(self):
        url = reverse('manager-restore-post', kwargs={'pk': self.pk})
        assert resolve(url).func.view_class == ManagerRestorePostConfirmView

    def test_manager_add_comment_url(self):
        url = reverse('manager-add-comment', kwargs={'pk': self.pk})
        assert resolve(url).func.view_class == ManagerAddCommentView


class TestEditorPanelUrls(object):
    """Test Class for Custom Admin app's (editor-panel) urls.
    Below test functions tests for all urls defined in custom_admin/urls.py
    """

    # PK for editor-post-update, editor-post-delete, editor-restore-post-confirm and editor-comment-list
    pk = 1

    def test_editor_panel_url(self):
        url = reverse('editor-panel')
        assert resolve(url).func.view_class == EditorMainPageView

    def test_editor_post_list_url(self):
        url = reverse('editor-post-list')
        assert resolve(url).func.view_class == EditorPostListView

    def test_editor_post_create_url(self):
        url = reverse('editor-post-create')
        assert resolve(url).func.view_class == EditorPostCreateView

    def test_editor_post_update_url(self):
        url = reverse('editor-post-update', kwargs={'pk': self.pk})
        assert resolve(url).func.view_class == EditorPostUpdateView

    def test_editor_post_delete_url(self):
        url = reverse('editor-post-delete', kwargs={'pk': self.pk})
        assert resolve(url).func.view_class == EditorPostDeleteView

    def test_editor_restore_post_list_url(self):
        url = reverse('editor-restore-post-list')
        assert resolve(url).func.view_class == EditorRestorePostListView

    def test_editor_restore_post_confirm_url(self):
        url = reverse('editor-restore-post-confirm', kwargs={'pk': self.pk})
        assert resolve(url).func.view_class == EditorRestorePostConfirmView

    def test_editor_comment_list_url(self):
        url = reverse('editor-comment-list', kwargs={'pk': self.pk})
        assert resolve(url).func.view_class == EditorCommentListView
