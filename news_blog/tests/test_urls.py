import pytest
from django.urls import reverse, resolve
from news_blog.views import (
    HomeView,
    PostDetailView,
    FollowView,
    NotificationSeenView,
    PostNotificationListView,
    AddViewsView,
    ManagerApplicationView,
    EditorApplicationView,
    PremiumApplyView,
    NotificationFromAdminView,
    NotificationFromAdminSeenView,
    StripeConfig,
    CreateCheckoutSession,
    SuccessPaymentView,
    FailedPaymentView,
    StripeWebhook
)


class TestNewsBlogUrls(object):
    """Test Class for News Blog app's urls.
    Below test functions tests for all urls defined in news_blog/urls.py
    """

    # PK for post-detail and follow urls
    pk = 1

    def test_home_url(self):
        url = reverse('home')
        assert resolve(url).func.__name__ == HomeView.as_view().__name__

    def test_post_detail_url(self):
        url = reverse('post-detail', kwargs={'pk': self.pk})
        assert resolve(url).func.__name__ == PostDetailView.as_view().__name__

    def test_follow_url(self):
        url = reverse('follow', kwargs={'pk': self.pk})
        assert resolve(url).func.__name__ == FollowView.as_view().__name__

    def test_notification_seen_url(self):
        url = reverse('notification-seen')
        assert resolve(url).func.__name__ == NotificationSeenView.as_view().__name__

    def test_notification_list_url(self):
        url = reverse('notification-list')
        assert resolve(url).func.__name__ == PostNotificationListView.as_view().__name__

    def test_add_views_url(self):
        url = reverse('add-views')
        assert resolve(url).func.__name__ == AddViewsView.as_view().__name__

    def test_apply_for_manager_url(self):
        url = reverse('apply-for-manager')
        assert resolve(url).func.__name__ == ManagerApplicationView.as_view().__name__

    def test_apply_for_editor_url(self):
        url = reverse('apply-for-editor')
        assert resolve(url).func.__name__ == EditorApplicationView.as_view().__name__

    def test_apply_for_premium_user_url(self):
        url = reverse('apply-for-premium-user')
        assert resolve(url).func.__name__ == PremiumApplyView.as_view().__name__

    def test_notification_from_admin_url(self):
        url = reverse('notification-from-admin')
        assert resolve(url).func.__name__ == NotificationFromAdminView.as_view().__name__

    def test_admin_notification_seen_url(self):
        url = reverse('admin-notification-seen')
        assert resolve(url).func.__name__ == NotificationFromAdminSeenView.as_view().__name__

    def test_stripe_config_url(self):
        url = reverse('stripe-config')
        assert resolve(url).func.__name__ == StripeConfig.as_view().__name__

    def test_create_checkout_session_url(self):
        url = reverse('create-checkout-session')
        assert resolve(url).func.__name__ == CreateCheckoutSession.as_view().__name__

    def test_success_url(self):
        url = reverse('success')
        assert resolve(url).func.__name__ == SuccessPaymentView.as_view().__name__

    def test_cancel_url(self):
        url = reverse('cancel')
        assert resolve(url).func.__name__ == FailedPaymentView.as_view().__name__

    def test_webhook_url(self):
        url = reverse('webhook')
        assert resolve(url).func.__name__ == StripeWebhook.as_view().__name__
