from django.test import TestCase, Client
from django.urls import reverse

from users.constants import WRONG_CREDENTIALS
from users.models import CustomUser as User, UserType
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from users.token import account_activation_token
from django.contrib.auth.models import Group
from django.core import mail
import pytest


class TestUsersViews(TestCase):
    def setUp(self):
        consumer_type = UserType.objects.create(name='consumer')
        self.user = User.objects.create_user(email='desaiparth971@gmail.com', password='Parth@2000')
        self.user.is_active = False
        self.user.user_type = consumer_type
        self.user.save()

        grp = Group.objects.create(name='consumer')
        grp.user_set.add(self.user)

        self.client = Client()

        self.register_url = reverse('register')
        self.profile_url = reverse('profile', kwargs={'pk': self.user.id})
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.password_reset = reverse('password-reset')
        self.password_reset_complete = reverse('password-reset-complete')

        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)
        self.password_reset_confirm = reverse('password-reset-confirm', args=[self.uidb64, self.token])
        self.activate = reverse('activate', args=[self.uidb64, self.token])

    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_logout_with_login_GET(self):
        self.user.is_active = True
        self.user.save()
        self.logged_in = self.client.login(email='desaiparth971@gmail.com', password='Parth@2000')

        self.assertEqual(self.logged_in, True)
        response = self.client.get(self.logout_url)
        expected_url = self.home_url
        self.assertRedirects(response, expected_url, status_code=302,
                             target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

    def test_logout_without_login_GET(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 403)

    def test_activate_GET(self):
        response = self.client.get(self.activate)
        expected_url = self.home_url
        self.assertRedirects(response, expected_url, status_code=302,
                             target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

    def test_profile_without_login_GET(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 403)

    def test_profile_with_login_GET(self):
        self.user.is_active = True
        self.user.save()
        self.logged_in = self.client.login(email='desaiparth971@gmail.com', password='Parth@2000')

        self.assertEqual(self.logged_in, True)

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_reset_password_GET(self):
        response = self.client.get(self.password_reset)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_reset.html')

    def test_login_POST(self):
        self.user.is_active = True
        self.user.save()

        response = self.client.post(self.login_url, {
            'email': 'desaiparth971@gmail.com',
            'password': 'Parth@2000'
        })

        self.assertRedirects(response, self.home_url, status_code=302,
                             target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

    # register POST remaining

    def test_logout_without_login_POST(self):
        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, 403)

    def test_logout_with_login_POST(self):
        self.user.is_active = True
        self.user.save()

        self.logged_in = self.client.login(email='desaiparth971@gmail.com', password='Parth@2000')

        self.assertEqual(self.logged_in, True)

        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, 405)

    def test_activate_email_POST(self):
        response = self.client.post(self.activate, {})
        self.assertEqual(response.status_code, 405)

    def test_reset_password_and_confirm_POST(self):
        # we post the response with our "email address"
        self.user.is_active = True
        self.user.save()

        response = self.client.post(self.password_reset, {'email': 'desaiparth971@gmail.com'})
        self.assertEqual(1, len(mail.outbox))
        #
        self.assertEqual(response.status_code, 302)
        # At this point the system will "send" us an email. We can "check" it.:
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'News Website Password Reset')

        # Now we post to the same url with our new password:
        response = self.client.post(
            self.password_reset_confirm,
            {'new_password1': 'Admin@2000', 'new_password2': 'Admin@2000'}
        )
        self.assertEqual(response.status_code, 200)

    def test_profile_POST(self):
        self.user.is_active = True
        self.user.save()

        self.logged_in = self.client.login(email='desaiparth971@gmail.com', password='Parth@2000')
        self.assertEqual(self.logged_in, True)

        response = self.client.post(self.profile_url, {
            'first_name': 'ParthUpdatedName',
            'last_name': 'last name updated',
            'age': 21,
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.first_name, 'ParthUpdatedName')
        self.assertEqual(user.last_name, 'last name updated')
        self.assertEqual(user.age, 21)

        self.assertRedirects(response, self.home_url, status_code=302,
                             target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)


class TestBug1(object):

    @pytest.mark.django_db
    def test_login_view_post_with_wrong_credentials(self, client):

        response = client.post(reverse('login'), {'email': 'fake@fake.com', 'password': 'parth2000'})
        assert response.status_code == 200
        messages = list(response.context['messages'])
        assert len(messages) == 1
        assert str(messages[0]) == WRONG_CREDENTIALS

    @pytest.mark.django_db
    @pytest.mark.xfail
    def test_register_view_post(self, client, create_user_types, create_groups):
        response = client.post(reverse('register'),
                               {'email': 'desaiparth971@gmail.com',
                                'password1': 'parth2000',
                                'password2': 'parth2000'
                                })
        assert response.status_code == 302

        response = client.post(reverse('register'),
                               {'email': 'desaiparth971@gmail.com',
                                'password1': 'parth2000',
                                'password2': 'parth'
                                })
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_activate_email_get(self, client):
        user = User.objects.create_user(email='desaiparth971@gmail.com', password='Parth@2000')
        uidb64 = urlsafe_base64_encode(force_bytes(12))
        token = account_activation_token.make_token(user)
        activate = reverse('activate', args=[uidb64, token])
        response = client.get(activate)
        assert response.status_code == 302

