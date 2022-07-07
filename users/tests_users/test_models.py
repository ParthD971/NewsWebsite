import pytest
from users.models import UserType


class TestUserTypeModel(object):
    @pytest.mark.django_db
    def test_name_lower_case(self, create_user_type_obj):
        user_type = create_user_type_obj(name='CAPITAL')
        assert user_type.name == 'capital'

    @pytest.mark.django_db
    def test_name(self, create_user_type_obj):
        user_type = create_user_type_obj(name='admin user')
        assert user_type.name == 'admin user'

    @pytest.mark.django_db
    def test_string(self, create_user_type_obj):
        user_type = create_user_type_obj(name='test')
        assert str(user_type) == 'test'

    @pytest.mark.django_db
    def test_max_length(self, create_user_type_obj):
        user_type = create_user_type_obj(name='test')
        max_length = user_type._meta.get_field('name').max_length
        assert max_length == 50


class TestUserModel(object):
    @pytest.mark.django_db
    def test_string(self, create_role_based_user):
        user = create_role_based_user(email='desaiparth@gmail.com')
        assert str(user) == 'consumer | desaiparth'

    @pytest.mark.django_db
    def test_username(self, create_role_based_user):
        user = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        assert user.username is None

    @pytest.mark.django_db
    def test_email(self, create_role_based_user):
        user = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        assert user.email == 'desaiparth@gmail.com'

    @pytest.mark.django_db
    def test_is_blocked(self, create_role_based_user):
        user = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        assert not user.is_blocked

    @pytest.mark.django_db
    def test_user_type(self, create_role_based_user):
        user = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        assert user.user_type.name == 'consumer'
        user = create_role_based_user(name='manager', email='manager@gmail.com')
        assert user.user_type.name == 'manager'

    @pytest.mark.django_db
    def test_age(self, create_role_based_user):
        user = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        assert user.age is None
        user = create_role_based_user(name='manager', email='manager@gmail.com', age=14)
        assert user.age == 14

    @pytest.mark.django_db
    def test_is_premium_user(self, create_role_based_user):
        user = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        assert not user.is_premium_user

    @pytest.mark.django_db
    def test_first_name(self, create_role_based_user):
        user = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        assert user.first_name == 'desaiparth'

    @pytest.mark.django_db
    def test_last_name(self, create_role_based_user):
        user = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        assert user.last_name == ''

    @pytest.mark.django_db
    def test_is_staff(self, create_role_based_user):
        user = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        assert not user.is_staff
        user = create_role_based_user(name='manager', email='desaiparth1@gmail.com', is_staff=True)
        assert user.is_staff
        user = create_role_based_user(name='editor', email='desaiparth2@gmail.com', is_staff=True)
        assert user.is_staff
        user = create_role_based_user(name='admin', email='desaiparth3@gmail.com', is_staff=True)
        assert user.is_staff




