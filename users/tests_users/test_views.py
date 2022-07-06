from django.test import TestCase, Client
from django.urls import reverse, resolve
from users.models import CustomUser as User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from users.token import account_activation_token
from django.contrib.auth.models import Group


class UsersTestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='desaiparth971@gmail.com', password='Parth@2000')
        self.user.is_active = False
        self.user.save()

        Group.objects.create(name='consumer')

        self.client = Client()
        self.register_url = reverse('register')
        self.profile_url = reverse('profile', args=[self.user.id])
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)
        self.activate = reverse('activate', args=[self.uidb64, self.token])

    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_logout_GET(self):
        response = self.client.get(self.logout_url)
        expected_url = self.home_url
        self.assertRedirects(response, expected_url, status_code=302,
                             target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

    def test_activate_GET(self):
        response = self.client.get(self.activate)
        expected_url = self.home_url
        self.assertRedirects(response, expected_url, status_code=302,
                             target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)
        self.assertTrue(self.user.is_active)
        print(self.user.groups.all())

    def test_profile_without_login_GET(self):
        response = self.client.get(self.profile_url)

        self.assertRedirects(response, status_code=403,
                             target_status_code=200)

    def test_profile_with_login_GET(self):
        self.logged_in = self.client.login(email='desaiparth971@gmail.com', password='Parth@2000')

        self.assertEquals(self.logged_in, True)

        response = self.client.get(self.profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')








    # def test_register_POST(self):
    #     response = self.client.post(self.register_url, {
    #         'username': 'testuser1',
    #         'email': 'testuser1@company.com',
    #         'password1': 'username123',
    #         'password2': 'username123',
    #     })
    #
    #     self.assertRedirects(response, self.login_url, status_code=302,
    #                          target_status_code=200, msg_prefix='',
    #                          fetch_redirect_response=True)
    #
    # def test_profile_without_login_POST(self):
    #     response = self.client.post(self.profile_url)
    #
    #     expected_url = self.login_url + '?next=' + self.profile_url
    #     self.assertRedirects(response, expected_url, status_code=302,
    #                          target_status_code=200, msg_prefix='',
    #                          fetch_redirect_response=True)
    #
    # def test_profile_with_login_with_data_POST(self):
    #     user = User.objects.create_user('testuser', 'testuser@company.com', 'testuser123')
    #
    #     self.logged_in = self.client.login(username='testuser', password='testuser123')
    #
    #     self.assertEquals(self.logged_in, True)
    #
    #     response = self.client.post(self.profile_url, {
    #         'username': 'updatedUsername',
    #         'email': 'updatedUsername@company.com',
    #     })
    #
    #     self.assertRedirects(response, self.profile_url, status_code=302,
    #                          target_status_code=200, msg_prefix='',
    #                          fetch_redirect_response=True)
    #
    # def test_profile_with_login_without_data_POST(self):
    #     user = User.objects.create_user('testuser', 'testuser@company.com', 'testuser123')
    #
    #     self.logged_in = self.client.login(username='testuser', password='testuser123')
    #
    #     self.assertEquals(self.logged_in, True)
    #
    #     response = self.client.post(self.profile_url)
    #
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'users/profile.html')
