from django.test import TestCase
from django.urls import reverse, resolve
from users.views import RegisterView
from django.contrib.auth import views as auth_views


class TestUrls(TestCase):
    def test_user_registration_with_valid_data(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'email': 'username@company.com',
            'password1': 'uniquePass@123',
            'password2': 'uniquePass@123'
        })

        self.assertTrue(form.is_valid())

    def test_user_registration_with_invalid_data(self):
        form = UserRegistrationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_user_update_with_valid_data(self):
        form = UserUpdateForm(data={
            'username': 'testuser',
            'email': 'username@company.com'
        })

        self.assertTrue(form.is_valid())

    def test_user_update_with_invalid_data(self):
        form = UserUpdateForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_profile_update_with_valid_data(self):
        form = ProfileUpdateForm(data={
            'image': 'default.jpg'
        })

        self.assertTrue(form.is_valid())

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_profile_update_with_invalid_data(self):
        from django.core.files.uploadedfile import InMemoryUploadedFile
        from io import BytesIO
        image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)),
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        form = ProfileUpdateForm(files={'image': image})
        self.assertTrue(form.is_valid())
