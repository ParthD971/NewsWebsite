from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import (
    RegisterView,
    LoginView,
    LogoutView,
    ActivateEmail,
    ResetPasswordView,
    ProfileView
)
from django.contrib.auth import views as auth_views


class TestUsersUrls(SimpleTestCase):
    """Test Class for Users app's urls.
    Below test functions tests for all urls defined in users/urls.py
    """

    # For activate email and password reset confirm urls.
    uidb64 = 'MQ'
    token = '463-9c763d2080d01c09b85c'

    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_activate_email_url(self):
        url = reverse('activate', args=[self.uidb64, self.token])
        self.assertEqual(resolve(url).func.view_class, ActivateEmail)

    def test_reset_password_url(self):
        url = reverse('password-reset')
        self.assertEqual(resolve(url).func.view_class, ResetPasswordView)

    def test_profile_url(self):
        url = reverse('profile', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProfileView)

    def test_password_reset_confirm_url(self):
        url = reverse('password-reset-confirm', args=[self.uidb64, self.token])
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)

    def test_password_reset_complete_url(self):
        url = reverse('password-reset-complete')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)
