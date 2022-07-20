import json

from django.conf import settings
from pytest_django.asserts import assertTemplateUsed, assertJSONEqual
import pytest
from django.shortcuts import reverse


class TestHomeView:
    """Test Class for HomeView."""

    @pytest.mark.django_db
    def test_get(
            self,
            get_data,
            client,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_obj,
            create_post_status_obj
    ):
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

        author = create_role_based_user(name='editor', email='desaiparth@gmail.com')
        create_post_obj(
            author=author,
            status=create_post_status_obj(name='active'),
            title='Apple in pie Breaking news'
        )

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse('home'), {'search': 'Apple'})
        assert len(response.context['posts']) == 1
        assert response.status_code == 200
        assertTemplateUsed(response, get_data['home'])

        response = cli.get(reverse('home'), {'author': 'desaiparth'})
        assert len(response.context['posts']) == 1
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

        consumer = create_role_based_user(name='consumer')
        post.premium = True
        post.save()
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse('post-detail', kwargs={'pk': post.id}))
        assert response.status_code == 302
        response = client.get(reverse('post-detail', kwargs={'pk': post.id}))
        assert response.status_code == 302


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

    @pytest.mark.django_db
    def test_post(
            self,
            get_data,
            client,
            create_role_based_user,
            auto_login_consumer_user,
            create_notification_type_obj,
            create_notification_status_obj
    ):
        consumer = create_role_based_user(name='consumer')
        create_notification_status_obj('pending')
        create_notification_type_obj(name='manager request')

        cli, user = auto_login_consumer_user(user=consumer)

        response = cli.post(reverse('apply-for-manager'), {'check': True})
        assert response.status_code == 302


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

    @pytest.mark.django_db
    def test_post(
            self,
            get_data,
            client,
            create_role_based_user,
            auto_login_consumer_user,
            create_notification_type_obj,
            create_notification_status_obj
    ):
        consumer = create_role_based_user(name='consumer')

        cli, user = auto_login_consumer_user(user=consumer)

        response = cli.post(reverse('apply-for-editor'), {'check': True})
        assert response.status_code == 302

        create_notification_type_obj(name='editor request')

        response = cli.post(reverse('apply-for-editor'), {'check': True})
        assert response.status_code == 302

        create_notification_status_obj('pending')

        response = cli.post(reverse('apply-for-editor'), {'check': True})
        assert response.status_code == 302


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


class TestFollowView:
    """Test Class for FollowView."""

    @pytest.mark.django_db
    def test_get(
            self,
            get_data,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_obj
    ):
        post = create_post_obj()

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse('follow', kwargs={'pk': post.id}), {'author_id': post.author.id})
        assert response.status_code == 302

        response = cli.get(reverse('follow', kwargs={'pk': post.id}), {'author_name': post.author_display_name})
        assert response.status_code == 302


class TestNotificationSeenView:
    """Test Class for NotificationSeenView."""

    @pytest.mark.django_db
    def test_get(
            self,
            get_data,
            create_role_based_user,
            auto_login_consumer_user,
            create_admin_notification_obj
    ):
        consumer = create_role_based_user(name='consumer')
        obj = create_admin_notification_obj(receiver=consumer)
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse('notification-seen'), {'pk': obj.id})


class TestAddViewsView:
    """Test Class for AddViewsView."""

    @pytest.mark.django_db
    def test_get(
            self,
            client,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_obj
    ):
        post = create_post_obj()

        response = client.get(reverse('add-views'), {'pk': post.id})

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse('add-views'), {'pk': post.id})
        post.refresh_from_db()
        assert post.views == 1


class TestStripeConfig:
    """Test Class for StripeConfig."""

    @pytest.mark.django_db
    def test_get(
            self,
            client
    ):
        response = client.get(reverse('stripe-config'))
        assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        )


class TestCreateCheckoutSession:
    """Test Class for CreateCheckoutSession."""

    @pytest.mark.django_db
    @pytest.mark.xfail
    def test_get(
            self,
            auto_login_consumer_user
    ):
        cli, user = auto_login_consumer_user()
        response = cli.get(reverse('create-checkout-session'))
        print(json.loads(response.content).get('error', None))
        assert json.loads(response.content).get('sessionId', None) is not None


class TestSuccessPaymentView:
    """Test Class for SuccessPaymentView."""

    @pytest.mark.django_db
    def test_get(
            self,
            create_role_based_user,
            auto_login_consumer_user
    ):
        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse('success'))
        assert response.status_code == 302


class TestFailedPaymentView:
    """Test Class for FailedPaymentView."""

    @pytest.mark.django_db
    def test_get(
            self,
            create_role_based_user,
            auto_login_consumer_user
    ):
        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse('cancel'))
        assert response.status_code == 302


class TestNotificationFromAdminSeenView:
    """Test Class for NotificationFromAdminSeenView."""

    @pytest.mark.django_db
    def test_get(
            self,
            create_admin_notification_obj,
            create_role_based_user,
            auto_login_consumer_user
    ):
        obj = create_admin_notification_obj()

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse('admin-notification-seen'), {'pk': obj.id})
        assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'msg': 'Done'}
        )

        response = cli.get(reverse('admin-notification-seen'), {'pk': 10})
        assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'msg': 'Does not exists'}
        )
