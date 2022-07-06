from django.test import TestCase
from django.urls import reverse, resolve
from users.models import CustomUser as User
from users import forms


class TestUsersForms(TestCase):
    def test_registration_form(self):
        """
        Test that ``RegistrationForm`` enforces email constraints,
        matching and short passwords.

        """
        sample_user = User.objects.create_user(
            password='Parth@2000',
            email='parth@gmail.com'
        )
        sample_user.save()

        invalid_data_dicts = [
            # Invalid Email.
            {
                'data':
                    {'email': 'invalidemailformat.com',
                     'password1': 'Parth@2000',
                     'password2': 'Parth@2000'},
                'error':
                    ('email', [u"Enter a valid email address."])
            },
            # Already-existing email.
            {
                'data':
                    {'email': 'parth@gmail.com',
                     'password1': 'Parth@2000',
                     'password2': 'Parth@2000'},
                'error':
                    ('email', [u"Email not valid."])
            },
            # Mismatched passwords.
            {
                'data':
                    {'email': 'parth@gmail.com',
                     'password1': 'Parth@2000',
                     'password2': 'bar'},
                'error':
                    ('password2', [u"The two password fields didn\'t match."])
            },
            # Short passwords.
            {
                'data':
                    {'email': 'parth@gmail.com',
                     'password1': 'foo',
                     'password2': 'foo'},
                'error':
                    ('password2', [u"This password is too short. It must contain at least 8 characters."])
            },
        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.RegisterForm(data=invalid_dict['data'])
            assert not form.is_valid()
            assert form.errors[invalid_dict['error'][0]] == invalid_dict['error'][1]

        form = forms.RegisterForm(data={'email': 'foo@example.com',
                                        'password1': 'foo',
                                        'password2': 'foo'})
        assert not form.is_valid()

    def test_login_form(self):
        """
        Test that ``LoginForm`` enforces email constraints,
        matching and short passwords.

        """
        sample_user = User.objects.create_user(
            password='Parth@2000',
            email='parth@gmail.com'
        )
        sample_user.save()

        invalid_data_dicts = [
            # Invalid Email.
            {
                'data':
                    {'email': 'invalid-email.com',
                     'password': 'Parth@2000'},
                'error':
                    ('email', [u"Enter a valid email address."])
            },
            # Not Registerd Email.
            {
                'data':
                    {'email': 'parth@gmail.com',
                     'password': 'Parth@2000'},
                'error':
                    ('email', [u"Email is not registered."])
            },
            # Empty Email.
            {
                'data':
                    {'email': '',
                     'password': 'Parth@2000'},
                'error':
                    ('email', [u"This field is required."])
            },
            # Empty Password.
            {
                'data':
                    {'email': 'invalid-email.com',
                     'password': ''},
                'error':
                    ('password', [u"This field is required."])
            },

        ]
        for invalid_dict in invalid_data_dicts:
            form = forms.LoginForm(data=invalid_dict['data'])
            assert not form.is_valid()
            assert form.errors[invalid_dict['error'][0]] == invalid_dict['error'][1]

        form = forms.LoginForm(data={'email': 'desai@gmail.com', 'password': 'Parth@2000'})

        assert not form.is_valid()
