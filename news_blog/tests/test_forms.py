import pytest
from news_blog.forms import ManagerApplicationForm
from news_blog.constants import ALREADY_ONE_ROLE_EXISTS


class TestManagerApplicationForm(object):

    @pytest.mark.django_db
    def test_not_checked(self):
        data = {
            'check': False
        }
        form = ManagerApplicationForm(data)
        assert not form.is_valid()
        assert form['check'].errors == ['This field is required.']

    @pytest.mark.django_db
    def test_role_already_exists(self, create_role_based_user, create_manager_application_obj):
        user = create_role_based_user(name='manager', email='desaiparth@gmail.com')
        create_manager_application_obj(user=user)

        class Request:
            def __init__(self, request_user):
                self.user = request_user

        data = {
            'check': True,
        }
        form = ManagerApplicationForm(data, request=Request(user))
        assert not form.is_valid()
        assert form['check'].errors == [ALREADY_ONE_ROLE_EXISTS % user.user_type.name]
