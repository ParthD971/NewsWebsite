from pytest_django.asserts import assertTemplateUsed
import pytest
from django.shortcuts import reverse


# class TestAdminPanel:
#     """Test Class for Admin Panel."""
#
#     @pytest.mark.django_db
#     @pytest.mark.parametrize('url_name', [
#         'admin-panel',
#         'admin-user-list',
#         'admin-categorie-list',
#         'admin-follow-list',
#         'admin-notification-status-list',
#         'admin-notification-type-list',
#         'admin-pcmiddle-list',
#         'admin-post-notification-list',
#         'admin-post-recycle-list',
#         'admin-post-status-record-list',
#         'admin-post-status-list',
#         'admin-post-view-list',
#         'admin-post-list',
#         'admin-user-type-list',
#         'admin-manager-comment-list',
#         'admin-notification-list',
#         'admin-send-notification',
#         'admin-application-notification-list',
#
#     ])
#     def test_get_permission(self, url_name, get_data, client, create_role_based_user, auto_login_consumer_user):
#         response = client.get(reverse(url_name))
#         assert response.status_code == 403
#
#         consumer = create_role_based_user(name='consumer')
#         cli, user = auto_login_consumer_user(user=consumer)
#         response = cli.get(reverse(url_name))
#         assert response.status_code == 403
#
#         user = create_role_based_user(name='admin')
#         cli, user = auto_login_consumer_user(user=user)
#         response = cli.get(reverse(url_name))
#         assert response.status_code == 200
#         assertTemplateUsed(response, get_data[url_name])
#
#     def test_get_user_update_view(self, get_data, client, create_role_based_user, auto_login_consumer_user):
#         url_name = 'admin-user-update'
#         consumer = create_role_based_user(name='consumer')
#
#         response = client.get(reverse(url_name, kwargs={'pk': consumer.id}))
#         assert response.status_code == 403
#
#         cli, user = auto_login_consumer_user(user=consumer)
#         response = cli.get(reverse(url_name, kwargs={'pk': consumer.id}))
#         assert response.status_code == 403
#
#         user = create_role_based_user(name='admin')
#         cli, user = auto_login_consumer_user(user=user)
#         response = cli.get(reverse(url_name, kwargs={'pk': consumer.id}))
#         assert response.status_code == 200
#         assertTemplateUsed(response, get_data[url_name])
#
#     def test_get_application_notification_update_view(
#             self,
#             get_data,
#             client,
#             create_role_based_user,
#             auto_login_consumer_user,
#             create_application_notification_obj
#     ):
#         url_name = 'admin-application-notification-update'
#
#         consumer = create_role_based_user(name='consumer')
#         notification = create_application_notification_obj(user=consumer)
#
#         response = client.get(reverse(url_name, kwargs={'pk': notification.id}))
#         assert response.status_code == 403
#
#         cli, user = auto_login_consumer_user(user=consumer)
#         response = cli.get(reverse(url_name, kwargs={'pk': notification.id}))
#         assert response.status_code == 403
#
#         user = create_role_based_user(name='admin')
#         cli, user = auto_login_consumer_user(user=user)
#         response = cli.get(reverse(url_name, kwargs={'pk': notification.id}))
#         assert response.status_code == 200
#         assertTemplateUsed(response, get_data[url_name])


class TestManagerPanel:
    """Test Class for Manager Panel."""

    @pytest.mark.django_db
    @pytest.mark.parametrize('url_name', [
        'manager-panel',
        'manager-post-list',
        'manager-categorie-list',
        'manager-categorie-create',
        'manager-user-list',
        'manager-restore-post-list',
    ])
    def test_get_permission(self, url_name, get_data, client, create_role_based_user, auto_login_consumer_user):
        response = client.get(reverse(url_name))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse(url_name))
        assert response.status_code == 403

        user = create_role_based_user(name='manager')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data[url_name])

    def test_get_post_update_view(
            self,
            get_data,
            client,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_obj
    ):
        url_name = 'manager-post-update'
        post = create_post_obj()

        response = client.get(reverse(url_name, kwargs={'pk': post.id}))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse(url_name, kwargs={'pk': post.id}))
        assert response.status_code == 403

        user = create_role_based_user(name='manager')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name, kwargs={'pk': post.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data[url_name])

    def test_get_categorie_update_view(
            self,
            get_data,
            client,
            create_role_based_user,
            auto_login_consumer_user,
            create_categorie_obj
    ):
        url_name = 'manager-categorie-update'
        category = create_categorie_obj(name='sports')

        response = client.get(reverse(url_name, kwargs={'pk': category.id}))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse(url_name, kwargs={'pk': category.id}))
        assert response.status_code == 403

        user = create_role_based_user(name='manager')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name, kwargs={'pk': category.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data[url_name])

    def test_get_user_update_view(
            self,
            get_data,
            client,
            create_role_based_user,
            auto_login_consumer_user
    ):
        url_name = 'manager-user-update'
        consumer = create_role_based_user(name='consumer')

        response = client.get(reverse(url_name, kwargs={'pk': consumer.id}))
        assert response.status_code == 403

        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse(url_name, kwargs={'pk': consumer.id}))
        assert response.status_code == 403

        user = create_role_based_user(name='manager')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name, kwargs={'pk': consumer.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data[url_name])

    def test_restore_post_view(
            self,
            get_data,
            client,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_recycle_obj
    ):
        url_name = 'manager-restore-post'

        obj = create_post_recycle_obj()

        response = client.get(reverse(url_name, kwargs={'pk': obj.id}))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse(url_name, kwargs={'pk': obj.id}))
        assert response.status_code == 403

        user = create_role_based_user(name='manager')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name, kwargs={'pk': obj.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data[url_name])

    def test_add_comment_view(
            self,
            get_data,
            client,
            create_role_based_user,
            auto_login_consumer_user,
            create_manager_comment_obj
    ):
        url_name = 'manager-add-comment'

        obj = create_manager_comment_obj()

        response = client.get(reverse(url_name, kwargs={'pk': obj.id}))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse(url_name, kwargs={'pk': obj.id}))
        assert response.status_code == 403

        user = create_role_based_user(name='manager')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name, kwargs={'pk': obj.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data[url_name])
