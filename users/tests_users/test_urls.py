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
    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.__name__, RegisterView.as_view().__name__)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.__name__, LoginView.as_view().__name__)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.__name__, LogoutView.as_view().__name__)

    def test_activate_email_url(self):
        uidb64 = 'MQ'
        token = '463-9c763d2080d01c09b85c'
        url = reverse('activate', args=[uidb64, token])
        self.assertEqual(resolve(url).func.__name__, ActivateEmail.as_view().__name__)

    def test_reset_password_url(self):
        url = reverse('password-reset')
        self.assertEqual(resolve(url).func.__name__, ResetPasswordView.as_view().__name__)

    def test_profile_url(self):
        url = reverse('profile', args=[1])
        self.assertEqual(resolve(url).func.__name__, ProfileView.as_view().__name__)

    def test_password_reset_confirm_url(self):
        uidb64 = 'MQ'
        token = '463-9c763d2080d01c09b85c'
        url = reverse('password-reset-confirm', args=[uidb64, token])
        self.assertEqual(resolve(url).func.__name__, auth_views.PasswordResetConfirmView.as_view().__name__)

    def test_password_reset_complete_url(self):
        url = reverse('password-reset-complete')
        self.assertEqual(resolve(url).func.__name__, auth_views.PasswordResetCompleteView.as_view().__name__)
