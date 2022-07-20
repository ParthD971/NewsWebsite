from pytest_django.asserts import assertTemplateUsed
import pytest
from django.shortcuts import reverse


class TestAdminPanel:
    """Test Class for Admin Panel."""

    @pytest.mark.django_db
    @pytest.mark.parametrize('url_name', [
        'admin-panel',
        'admin-user-list',
        'admin-categorie-list',
        'admin-follow-list',
        'admin-notification-status-list',
        'admin-notification-type-list',
        'admin-pcmiddle-list',
        'admin-post-notification-list',
        'admin-post-recycle-list',
        'admin-post-status-record-list',
        'admin-post-status-list',
        'admin-post-view-list',
        'admin-post-list',
        'admin-user-type-list',
        'admin-manager-comment-list',
        'admin-notification-list',
        'admin-send-notification',
        'admin-application-notification-list',

    ])
    def test_get_permission(self, url_name, get_data, client, create_role_based_user, auto_login_consumer_user):
        response = client.get(reverse(url_name))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse(url_name))
        assert response.status_code == 403

        user = create_role_based_user(name='admin')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data[url_name])

    def test_get_user_update_view(self, get_data, client, create_role_based_user, auto_login_consumer_user):
        url_name = 'admin-user-update'
        consumer = create_role_based_user(name='consumer')

        response = client.get(reverse(url_name, kwargs={'pk': consumer.id}))
        assert response.status_code == 403

        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse(url_name, kwargs={'pk': consumer.id}))
        assert response.status_code == 403

        user = create_role_based_user(name='admin')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name, kwargs={'pk': consumer.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data[url_name])

    def test_get_application_notification_update_view(
            self,
            get_data,
            client,
            create_role_based_user,
            auto_login_consumer_user,
            create_application_notification_obj
    ):
        url_name = 'admin-application-notification-update'

        consumer = create_role_based_user(name='consumer')
        notification = create_application_notification_obj(user=consumer)

        response = client.get(reverse(url_name, kwargs={'pk': notification.id}))
        assert response.status_code == 403

        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse(url_name, kwargs={'pk': notification.id}))
        assert response.status_code == 403

        user = create_role_based_user(name='admin')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name, kwargs={'pk': notification.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data[url_name])

    def test_admin_user_list_view_filter(self, create_role_based_user, auto_login_consumer_user):
        parth = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        rahul = create_role_based_user(name='consumer', email='rahul@gmail.com')
        user = create_role_based_user(name='admin')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse('admin-user-list'), {'search': 'parth'})
        assert response.context['users'][0] == parth
        assert response.status_code == 200

        response = cli.get(reverse('admin-user-list'), {'blocked': 'True'})
        assert not response.context['users']
        assert response.status_code == 200

        manager = create_role_based_user(name='manager')
        response = cli.get(reverse('admin-user-list'), {'staff': 'True'})
        assert response.context['users'][0] == manager
        assert response.status_code == 200

        rahul.is_premium_user = True
        rahul.save()
        response = cli.get(reverse('admin-user-list'), {'premium_user': 'True'})
        assert response.context['users'][0] == rahul
        assert response.status_code == 200

        response = cli.get(reverse('admin-user-list'), {'active': 'True'})
        assert len(response.context['users']) == 3
        assert response.status_code == 200

        response = cli.get(reverse('admin-user-list'), {'user_type': 'editor'})
        assert len(response.context['users']) == 0
        response = cli.get(reverse('admin-user-list'), {'user_type': 'manager'})
        assert len(response.context['users']) == 1
        assert response.status_code == 200

    def test_admin_application_notification_list_view_filter(
            self,
            create_role_based_user,
            auto_login_consumer_user,
            create_application_notification_obj
    ):
        parth = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        create_role_based_user(name='consumer', email='rahul@gmail.com')

        notifications_obj = create_application_notification_obj(user=parth)

        user = create_role_based_user(name='admin')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse('admin-application-notification-list'), {'search': 'parth'})
        assert response.context['notifications'][0] == notifications_obj
        assert response.status_code == 200

        response = cli.get(reverse('admin-application-notification-list'), {'request_for': 'editor'})
        assert response.context['notifications'][0] == notifications_obj
        assert response.status_code == 200

    def test_admin_application_notification_update_view_filter(
            self,
            create_role_based_user,
            auto_login_consumer_user,
            create_application_notification_obj,
            create_notification_status_obj
    ):

        notification = create_application_notification_obj()
        accepted = create_notification_status_obj(name='accepted')

        user = create_role_based_user(name='admin')
        cli, user = auto_login_consumer_user(user=user)
        data = {
            'status': accepted.id
        }
        url = reverse('admin-application-notification-update', kwargs={'pk': notification.id})
        response = cli.post(url, data)
        assert response.status_code == 302


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

    def test_post_list_view(
            self,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_obj
    ):
        editor = create_role_based_user(name='editor')
        create_post_obj(title='apple Pie breaking news')
        create_post_obj(author=editor)

        user = create_role_based_user(name='manager')
        cli, user = auto_login_consumer_user(user=user)
        url_name = 'manager-post-list'
        response = cli.get(reverse(url_name), {'search': 'apple'})
        assert len(response.context['posts']) == 1
        assert response.status_code == 200

        response = cli.get(reverse(url_name), {'status': 'pending'})
        assert len(response.context['posts']) == 2
        assert response.status_code == 200

        response = cli.get(reverse(url_name), {'editor': editor.first_name})
        assert len(response.context['posts']) == 1
        assert response.status_code == 200

    def test_post_update_view(
            self,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_obj,
            create_post_status_obj,
            create_categorie_obj,
            create_notification_type_obj
    ):
        editor = create_role_based_user(name='editor')
        pending = create_post_status_obj(name='pending')
        active = create_post_status_obj(name='active')
        inactive = create_post_status_obj(name='inactive')
        deleted = create_post_status_obj(name='deleted')
        inreview = create_post_status_obj(name='inreview')
        rejected = create_post_status_obj(name='rejected')
        create_notification_type_obj(name='post added')
        create_notification_type_obj(name='post deleted')
        sports = create_categorie_obj(name='sports')
        post1 = create_post_obj(title='apple Pie breaking news')
        create_post_obj(author=editor)

        user = create_role_based_user(name='manager')
        cli, user = auto_login_consumer_user(user=user)
        url_name = 'manager-post-update'
        response = cli.post(reverse(url_name, kwargs={'pk': post1.id}), {
            'title': 'title',
            'content': 'content',
            'category': [sports.id],
            'status': active.id
        })
        assert response.status_code == 302

        post1.status = active
        post1.save()
        response = cli.post(reverse(url_name, kwargs={'pk': post1.id}), {
            'title': 'title',
            'content': 'content',
            'category': [sports.id],
            'status': inactive.id
        })
        assert response.status_code == 302

        post1.status = inactive
        post1.save()
        response = cli.post(reverse(url_name, kwargs={'pk': post1.id}), {
            'title': 'title',
            'content': 'content',
            'category': [sports.id],
            'status': deleted.id
        })
        assert response.status_code == 302

        post1.status = pending
        post1.save()
        response = cli.post(reverse(url_name, kwargs={'pk': post1.id}), {
            'title': 'title',
            'content': 'content',
            'category': [sports.id],
            'status': inreview.id
        })
        assert response.status_code == 302

        post1.status = pending
        post1.save()
        response = cli.post(reverse(url_name, kwargs={'pk': post1.id}), {
            'title': 'title',
            'content': 'content',
            'category': [sports.id],
            'status': rejected.id
        })
        assert response.status_code == 302

    def test_user_list_view(
            self,
            create_role_based_user,
            auto_login_consumer_user
    ):
        create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        create_role_based_user(name='editor')

        user = create_role_based_user(name='manager')
        cli, user = auto_login_consumer_user(user=user)
        url_name = 'manager-user-list'
        response = cli.get(reverse(url_name), {'blocked': True})
        assert len(response.context['users']) == 0
        assert response.status_code == 200

        response = cli.get(reverse(url_name), {'search': 'parth'})
        assert len(response.context['users']) == 1
        assert response.status_code == 200

        response = cli.get(reverse(url_name), {'staff': True})
        assert len(response.context['users']) == 1
        assert response.status_code == 200

        response = cli.get(reverse(url_name), {'active': True})
        assert len(response.context['users']) == 2
        assert response.status_code == 200

    def test_restore_post_view_bug1(
            self,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_recycle_obj,
            create_post_status_obj
    ):
        url_name = 'manager-restore-post'

        obj = create_post_recycle_obj()
        create_post_status_obj(name='inactive')

        user = create_role_based_user(name='manager')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.post(reverse(url_name, kwargs={'pk': obj.id}), {'check': True})
        assert response.status_code == 302

    def test_add_comment_view_bug1(
            self,
            create_role_based_user,
            auto_login_consumer_user,
            create_manager_comment_obj
    ):
        url_name = 'manager-add-comment'

        obj = create_manager_comment_obj()
        post = obj.post
        post.author = None
        post.post_type = 'MANUAL'
        post.save()

        user = create_role_based_user(name='manager')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name, kwargs={'pk': 10}))
        assert response.status_code == 200
        assertTemplateUsed(response, '404.html')

        cli, user = auto_login_consumer_user(user=user)
        response = cli.post(reverse(url_name, kwargs={'pk': post.id}), {'comment': 'comment'})
        assert response.status_code == 302


class TestEditorPanel:
    """Test Class for Editor Panel."""

    @pytest.mark.django_db
    @pytest.mark.parametrize('url_name', [
        'editor-panel',
        'editor-post-list',
        'editor-post-create',
        'editor-restore-post-list',
    ])
    def test_get_permission(self, url_name, get_data, client, create_role_based_user, auto_login_consumer_user):
        response = client.get(reverse(url_name))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse(url_name))
        assert response.status_code == 403

        user = create_role_based_user(name='editor')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data[url_name])

    def test_post_update_view(
            self,
            get_data,
            client,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_obj
    ):
        url_name = 'editor-post-update'
        post = create_post_obj()

        response = client.get(reverse(url_name, kwargs={'pk': post.id}))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse(url_name, kwargs={'pk': post.id}))
        assert response.status_code == 403

        user = create_role_based_user(name='editor')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name, kwargs={'pk': post.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data[url_name])

    def test_post_delete_view(
            self,
            get_data,
            client,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_obj
    ):
        url_name = 'editor-post-delete'
        post = create_post_obj()

        response = client.get(reverse(url_name, kwargs={'pk': post.id}))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse(url_name, kwargs={'pk': post.id}))
        assert response.status_code == 403

        user = create_role_based_user(name='editor')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name, kwargs={'pk': post.id}))
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
        url_name = 'editor-restore-post-confirm'

        obj = create_post_recycle_obj()

        response = client.get(reverse(url_name, kwargs={'pk': obj.id}))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse(url_name, kwargs={'pk': obj.id}))
        assert response.status_code == 403

        user = create_role_based_user(name='editor')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name, kwargs={'pk': obj.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data[url_name])

    def test_comment_list_view(
            self,
            get_data,
            client,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_obj
    ):
        url_name = 'editor-comment-list'

        post = create_post_obj()

        response = client.get(reverse(url_name, kwargs={'pk': post.id}))
        assert response.status_code == 403

        consumer = create_role_based_user(name='consumer')
        cli, user = auto_login_consumer_user(user=consumer)
        response = cli.get(reverse(url_name, kwargs={'pk': post.id}))
        assert response.status_code == 403

        user = create_role_based_user(name='editor')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.get(reverse(url_name, kwargs={'pk': post.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, get_data[url_name])

    def test_post_list_view(
            self,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_obj,
            create_categorie_obj,
            create_post_status_obj
    ):
        sports = create_categorie_obj(name='sports')
        politics = create_categorie_obj(name='politics')
        user = create_role_based_user(name='editor')

        post1 = create_post_obj(author=user)
        post1.category.add(sports)
        post2 = create_post_obj(author=user, title='apple pie breaking news')
        post2.category.add(politics)

        cli, user = auto_login_consumer_user(user=user)
        url_name = 'editor-post-list'
        response = cli.get(reverse(url_name))
        assert response.status_code == 200

        response = cli.get(reverse(url_name), {'search': 'apple'})
        assert response.context.get('posts')[0] == post2
        assert response.status_code == 200

        response = cli.get(reverse(url_name), {'status': 'pending'})
        assert len(response.context.get('posts')) == 2
        assert response.status_code == 200

    def test_post_create_view(
            self,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_obj,
            create_categorie_obj,
            create_post_status_obj
    ):
        sports = create_categorie_obj(name='sports')
        politics = create_categorie_obj(name='politics')
        user = create_role_based_user(name='editor')
        create_post_status_obj(name='pending')

        cli, user = auto_login_consumer_user(user=user)
        url_name = 'editor-post-create'
        response = cli.post(reverse(url_name), {
            'title': 'New title',
            'content': 'content',
            'category': [sports.id, politics.id]

        })
        assert response.status_code == 302

    def test_post_update_view_bug1(
            self,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_obj,
            create_categorie_obj,
            create_post_status_obj
    ):
        sports = create_categorie_obj(name='sports')
        politics = create_categorie_obj(name='politics')
        user = create_role_based_user(name='editor')
        create_post_status_obj(name='pending')
        post = create_post_obj(author=user)

        cli, user = auto_login_consumer_user(user=user)
        url_name = 'editor-post-update'
        response = cli.post(reverse(url_name, kwargs={'pk': post.id}), {
            'title': 'Updated',
            'content': 'updated content',
            'category': [sports.id, politics.id]

        })
        assert response.status_code == 302

    def test_post_delete_view_bug1(
            self,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_obj,
            create_post_status_obj
    ):
        url_name = 'editor-post-delete'
        post = create_post_obj()
        create_post_status_obj(name='deleted')

        editor = create_role_based_user(name='editor')
        cli, user = auto_login_consumer_user(user=editor)
        response = cli.post(reverse(url_name, kwargs={'pk': post.id}), {'check': True})
        assert response.status_code == 302

    def test_restore_post_view_bug1(
            self,
            create_role_based_user,
            auto_login_consumer_user,
            create_post_recycle_obj,
            create_post_status_obj
    ):
        url_name = 'editor-restore-post-confirm'

        obj = create_post_recycle_obj()
        create_post_status_obj(name='pending')

        user = create_role_based_user(name='editor')
        cli, user = auto_login_consumer_user(user=user)
        response = cli.post(reverse(url_name, kwargs={'pk': obj.id}), {'check': True})
        assert response.status_code == 302
