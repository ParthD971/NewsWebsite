import pytest


class TestManagerCommentModel(object):
    """Test Class for ManagerComment model."""

    @pytest.mark.django_db
    def test_string(self, create_manager_comment_obj, create_post_obj, create_role_based_user):
        """Testcase: This testcase tests string method of ManagerComment Model Class."""

        post = create_post_obj(
            title='Test Title',
            content='Test Content',
            author_display_name='Display Name'
        )
        manager = create_role_based_user(name='manager', email='desaiparth@gmail.com')
        obj = create_manager_comment_obj(post=post, manager=manager)

        assert str(obj) == ' | '.join([manager.first_name, post.title])

    @pytest.mark.django_db
    def test_field_values(self, create_manager_comment_obj, create_post_obj, create_role_based_user):
        """Testcase: This testcase tests field values."""

        post = create_post_obj(
            title='Test Title',
            content='Test Content',
            author_display_name='Display Name'
        )
        manager = create_role_based_user(name='manager', email='desaiparth@gmail.com')
        obj = create_manager_comment_obj(post=post, manager=manager, comment='Comment Content')

        assert obj.post == post
        assert obj.manager == manager
        assert obj.comment == 'Comment Content'


class TestAdminNotificationModel(object):
    """Test Class for AdminNotification model."""

    @pytest.mark.django_db
    def test_string(self, create_admin_notification_obj, create_role_based_user):
        """Testcase: This testcase tests string method of AdminNotification Model Class."""

        manager = create_role_based_user(name='manager')
        editor = create_role_based_user(name='editor')
        consumer = create_role_based_user(name='consumer')

        obj = create_admin_notification_obj(receiver=manager)
        assert str(obj) == manager.first_name
        obj = create_admin_notification_obj(receiver=editor)
        assert str(obj) == editor.first_name
        obj = create_admin_notification_obj(receiver=consumer)
        assert str(obj) == consumer.first_name

    @pytest.mark.django_db
    def test_field_values(self, create_admin_notification_obj, create_role_based_user):
        """Testcase: This testcase tests field values."""

        manager = create_role_based_user(name='manager')
        editor = create_role_based_user(name='editor')
        consumer = create_role_based_user(name='consumer')

        obj = create_admin_notification_obj(receiver=manager, message='Manager message')
        assert obj.receiver == manager
        assert obj.message == 'Manager message'
        assert not obj.seen

        obj = create_admin_notification_obj(receiver=editor, message='Editor message')
        assert obj.receiver == editor
        assert obj.message == 'Editor message'
        assert not obj.seen

        obj = create_admin_notification_obj(receiver=consumer, message='Consumer message')
        assert obj.receiver == consumer
        assert obj.message == 'Consumer message'
        assert not obj.seen
