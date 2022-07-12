from users.models import CustomUser as User
import pytest


class TestUsersManagers(object):
    """Test Class for CustomUserManager Manager."""

    @pytest.mark.django_db
    def test_create_user(self):
        """Testcase: This test case tests create_user method for
        - value of email attribute.
        - value of is_active attribute.
        - value of is_staff attribute.
        - value of is_superuser attribute.
        - value of username attribute.
        - error for invalid parameters passed in create_user method.
        """

        user = User.objects.create_user(email='normal@user.com', password='foo')
        assert user.email == 'normal@user.com'
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        assert user.username is None

        with pytest.raises(TypeError):
            User.objects.create_user()
        with pytest.raises(TypeError):
            User.objects.create_user(email='')
        with pytest.raises(ValueError):
            User.objects.create_user(email='', password="abc")

    @pytest.mark.django_db
    def test_create_superuser(self, create_user_type_obj, create_group_obj):
        """Testcase: This test case tests create_superuser method  for
        - value of email attribute.
        - value of is_active attribute.
        - value of is_staff attribute.
        - value of is_superuser attribute.
        - value of username attribute.
        - error for invalid parameters passed in create_superuser method.
        """

        create_user_type_obj(name='admin')
        create_group_obj(name='admin')

        admin_user = User.objects.create_superuser(email='super@user.com', password='abc')
        assert admin_user.email == 'super@user.com'
        assert admin_user.is_active
        assert admin_user.is_staff
        assert admin_user.is_superuser
        assert admin_user.username is None

        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email='super@user.com',
                password='foo',
                is_superuser=False
            )
