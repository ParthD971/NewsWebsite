from pytest_django.asserts import assertTemplateUsed
import pytest
from django.shortcuts import reverse


class TestHomeView:
    """Test Class for HomeView."""

    @pytest.mark.django_db
    def test_get(self, get_data, client, create_role_based_user, auto_login_consumer_user):
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data['home'])

        manager = create_role_based_user(name='manager')
        cli, user = auto_login_consumer_user(user=manager)
        response = cli.get(reverse('home'))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data['home'])

        editor = create_role_based_user(name='editor')
        cli, user = auto_login_consumer_user(user=editor)
        response = cli.get(reverse('home'))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data['home'])

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse('home'))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data['home'])


class TestPostDetailView:
    """Test Class for PostDetailView."""

    @pytest.mark.django_db
    def test_get(self, get_data, client, create_role_based_user, auto_login_consumer_user, create_post_obj, create_post_status_obj):
        post = create_post_obj()

        response = client.get(reverse('post-detail', kwargs={'pk': post.id}))
        assert response.status_code == 404

        post = create_post_obj(status=create_post_status_obj(name='active'))

        response = client.get(reverse('post-detail', kwargs={'pk': post.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data['post-detail'])

        manager = create_role_based_user(name='manager')
        cli, user = auto_login_consumer_user(user=manager)
        response = cli.get(reverse('post-detail', kwargs={'pk': post.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data['post-detail'])

        editor = create_role_based_user(name='editor')
        cli, user = auto_login_consumer_user(user=editor)
        response = cli.get(reverse('post-detail', kwargs={'pk': post.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data['post-detail'])

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse('post-detail', kwargs={'pk': post.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data['post-detail'])


class TestPostNotificationListView:
    """Test Class for PostNotificationListView."""

    @pytest.mark.django_db
    def test_get(self, get_data, client, create_role_based_user, auto_login_consumer_user):
        response = client.get(reverse('notification-list'))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)

        response = cli.get(reverse('notification-list'))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data['notification-list'])


class TestManagerApplicationView:
    """Test Class for ManagerApplicationView."""

    @pytest.mark.django_db
    def test_get(self, get_data, client, create_role_based_user, auto_login_consumer_user):
        response = client.get(reverse('apply-for-manager'))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)

        response = cli.get(reverse('apply-for-manager'))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data['apply-for-manager'])


class TestEditorApplicationView:
    """Test Class for EditorApplicationView."""

    @pytest.mark.django_db
    def test_get(self, get_data, client, create_role_based_user, auto_login_consumer_user):
        response = client.get(reverse('apply-for-editor'))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)

        response = cli.get(reverse('apply-for-editor'))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data['apply-for-editor'])


class TestPremiumApplyView:
    """Test Class for PremiumApplyView."""

    @pytest.mark.django_db
    def test_get(self, get_data, client, create_role_based_user, auto_login_consumer_user):
        response = client.get(reverse('apply-for-premium-user'))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)

        response = cli.get(reverse('apply-for-premium-user'))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data['apply-for-premium-user'])


class TestNotificationFromAdminView:
    """Test Class for NotificationFromAdminView."""

    @pytest.mark.django_db
    def test_get(self, get_data, client, create_role_based_user, auto_login_consumer_user):
        response = client.get(reverse('notification-from-admin'))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)

        response = cli.get(reverse('notification-from-admin'))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data['notification-from-admin'])




