from users import forms
import pytest


class TestLoginForm(object):
    """Test Class for LoginForm in users/forms.py"""

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ('invalid_data', 'error'),
        [
            # Email incorrect format
            (
                    {'email': 'invalid-email.com', 'password': 'Parth@2000'},
                    ('email', [u"Enter a valid email address."])
            ),
            # Email not registered
            (
                    {'email': 'notregister@gmail.com', 'password': 'Parth@2000'},
                    ('email', [u"Email is not registered."])
            ),
            # Email empty
            (
                    {'email': '', 'password': 'Parth@2000'},
                    ('email', [u"This field is required."])
            ),
            # Password empty
            (
                    {'email': 'invalid-email.com', 'password': ''},
                    ('password', [u"This field is required."])
            )
        ]
    )
    def test_login_form_errors(self, invalid_data, error, client):
        """Test Case: Login Form for invalid form-data."""

        form = forms.LoginForm(data=invalid_data)
        assert not form.is_valid()
        assert form.errors[error[0]] == error[1]

    @pytest.mark.django_db
    def test_login_form(self, create_role_based_user, test_password):
        """Test Case: Login Form for valid form-data."""

        user = create_role_based_user(name='consumer', email='parth@gmail.com')
        form = forms.LoginForm(data={'email': user.email, 'password': test_password})
        assert form.is_valid()


class TestRegisterForm(object):
    """Test Class for RegisterForm in users/forms.py"""

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ('invalid_data', 'error'),
        [
            # Invalid Email
            (
                    {'email': 'invalidemailformat.com', 'password1': 'Parth@2000', 'password2': 'Parth@2000'},
                    ('email', [u"Enter a valid email address."])
            ),
            # Non Existing Email
            (
                    {'email': 'parth@gmail.com', 'password1': 'Parth@2000', 'password2': 'Parth@2000'},
                    ('email', [u"Email not valid."])
            ),
            # Password miss-match
            (
                    {'email': 'parth@gmail.com', 'password1': 'Parth@2000', 'password2': 'abc'},
                    ('password2', [u"The two password fields didn\'t match."])
            ),
            # Short password
            (
                    {'email': 'parth@gmail.com', 'password1': 'desai', 'password2': 'desai'},
                    ('password2', [u"This password is too short. It must contain at least 8 characters."])
            ),
            # Common password
            (
                    {'email': 'parth@gmail.com', 'password1': 'password1234', 'password2': 'password1234'},
                    ('password2', [u"This password is too common."])
            )
        ]
    )
    def test_register_form_errors(self, invalid_data, error, client):
        """Test Case: Registration Form for invalid form-data."""

        form = forms.RegisterForm(data=invalid_data)
        assert not form.is_valid()
        assert form.errors[error[0]] == error[1]

    @pytest.mark.django_db
    def test_register_form(self, test_password):
        """Test Case: Registration Form for valid form-data."""

        form = forms.RegisterForm(data={
            'email': 'desaiparth971@gmail.com',
            'password1': test_password,
            'password2': test_password
        })
        assert form.is_valid()

    @pytest.mark.django_db
    def test_register_form_save(self, test_password, create_user_type_obj, create_group_obj):
        consumer_user_type = create_user_type_obj(name='consumer')
        consumer_group = create_group_obj(name='consumer')

        form = forms.RegisterForm(data={
            'email': 'desaiparth971@gmail.com',
            'password1': test_password,
            'password2': test_password
        })
        assert form.is_valid()
        user = form.save()
        assert not user.is_active
        assert user.user_type == consumer_user_type
        assert user.groups.first() == consumer_group


class TestProfileForm(object):
    """Test Class for ProfileForm in users/forms.py"""

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ('invalid_data', 'error'),
        [
            # First name Empty
            (
                    {'first_name': '', 'last_name': '', 'age': 21},
                    ('first_name', [u"This field is required."])
            ),
            # Age negative
            (
                    {'first_name': 'Parth', 'last_name': '', 'age': -1},
                    ('age', [u"Age not valid."])
            ),
            # Age zero
            (
                    {'first_name': 'Parth', 'last_name': '', 'age': 0},
                    ('age', [u"Age not valid."])
            ),
            # Age greater than 100
            (
                    {'first_name': 'Parth', 'last_name': '', 'age': 101},
                    ('age', [u"Age not valid."])
            ),

        ]
    )
    def test_profile_form_errors(self, invalid_data, error, client):
        """Test Case: Profile Form for invalid form-data."""

        form = forms.ProfileForm(data=invalid_data)
        assert not form.is_valid()
        assert form.errors[error[0]] == error[1]

    @pytest.mark.django_db
    def test_profile_form(self):
        """Test Case: Profile Form for valid form-data."""

        form = forms.ProfileForm(data={'first_name': 'Parth', 'last_name': 'Desai', 'age': 21})
        assert form.is_valid()
        assert form.is_valid()
        form = forms.ProfileForm(data={'first_name': 'Parth', 'last_name': '', 'age': 21})
        assert form.is_valid()
        form = forms.ProfileForm(data={'first_name': 'Parth', 'last_name': 'Desai'})
        assert form.is_valid()
