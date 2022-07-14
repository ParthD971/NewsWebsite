from news_blog.forms import ManagerApplicationForm, EditorApplicationForm
from news_blog.constants import ALREADY_ONE_ROLE_EXISTS, ALREADY_APPLIED_FOR__ROLE, NOTIFICATION_TYPE_MANAGER_REQUEST, \
    NOTIFICATION_TYPE_EDITOR_REQUEST
from users.constants import USER_TYPE_MANAGER, USER_TYPE_EDITOR


class Request:
    """Fake Request Class to send with Form initialization.
    Usually to pass some data in wsgi-request like user.
    """

    def __init__(self, request_user):
        self.user = request_user


class TestManagerApplicationForm(object):
    """Test Class for ManagerApplicationForm."""

    def test_not_checked(self):
        """Testcase: To test error for check field."""
        
        data = {
            'check': False
        }
        form = ManagerApplicationForm(data)
        assert not form.is_valid()
        assert form['check'].errors == ['This field is required.']

    def test_role_already_exists(self, create_role_based_user):
        """Testcase: To test error when user is already manager or editor."""

        manager_user = create_role_based_user(name='manager')
        editor_user = create_role_based_user(name='editor')

        data = {
            'check': True,
        }

        form = ManagerApplicationForm(data, request=Request(manager_user))
        assert not form.is_valid()
        assert form['check'].errors == [ALREADY_ONE_ROLE_EXISTS % manager_user.user_type.name]

        form = ManagerApplicationForm(data, request=Request(editor_user))
        assert not form.is_valid()
        assert form['check'].errors == [ALREADY_ONE_ROLE_EXISTS % editor_user.user_type.name]

    def test_already_applied_for_manager(self, create_role_based_user, create_application_notification_obj):
        """Testcase: To test error when user has already
        applied for manager post and try to apply again."""

        consumer_user = create_role_based_user(name='consumer')
        application = create_application_notification_obj(
            user=consumer_user,
            notification_type=NOTIFICATION_TYPE_MANAGER_REQUEST
        )

        data = {
            'check': True,
        }

        form = ManagerApplicationForm(data, request=Request(consumer_user))
        assert not form.is_valid()
        assert form['check'].errors == [ALREADY_APPLIED_FOR__ROLE % (USER_TYPE_MANAGER, application.status.name)]

    def test_already_applied_for_editor(self, create_role_based_user, create_application_notification_obj):
        """Testcase: To test error when user has applied for editor role
        and try to apply for manager while editor application is not rejected yet."""

        consumer_user = create_role_based_user(name='consumer')
        application = create_application_notification_obj(user=consumer_user)

        data = {
            'check': True,
        }

        form = ManagerApplicationForm(data, request=Request(consumer_user))
        assert not form.is_valid()
        assert form['check'].errors == [ALREADY_APPLIED_FOR__ROLE % (USER_TYPE_EDITOR, application.status.name)]

    def test_valid_form(self, create_role_based_user):
        """Testcase: To test form is valid."""

        consumer_user = create_role_based_user(name='consumer')

        data = {
            'check': True,
        }

        form = ManagerApplicationForm(data, request=Request(consumer_user))
        assert form.is_valid()


class TestEditorApplicationForm(object):
    """Test Class for EditorApplicationForm."""

    def test_not_checked(self):
        """Testcase: To test error for check field."""

        data = {
            'check': False
        }
        form = EditorApplicationForm(data)
        assert not form.is_valid()
        assert form['check'].errors == ['This field is required.']

    def test_role_already_exists(self, create_role_based_user):
        """Testcase: To test error when user is already manager or editor."""

        manager_user = create_role_based_user(name='manager')
        editor_user = create_role_based_user(name='editor')

        data = {
            'check': True,
        }

        form = EditorApplicationForm(data, request=Request(manager_user))
        assert not form.is_valid()
        assert form['check'].errors == [ALREADY_ONE_ROLE_EXISTS % manager_user.user_type.name]

        form = EditorApplicationForm(data, request=Request(editor_user))
        assert not form.is_valid()
        assert form['check'].errors == [ALREADY_ONE_ROLE_EXISTS % editor_user.user_type.name]

    def test_already_applied_for_editor(self, create_role_based_user, create_application_notification_obj):
        """Testcase: To test error when user has already
        applied for editor post and try to apply again."""

        consumer_user = create_role_based_user(name='consumer')
        application = create_application_notification_obj(
            user=consumer_user,
            notification_type=NOTIFICATION_TYPE_EDITOR_REQUEST
        )

        data = {
            'check': True,
        }

        form = EditorApplicationForm(data, request=Request(consumer_user))
        assert not form.is_valid()
        assert form['check'].errors == [ALREADY_APPLIED_FOR__ROLE % (USER_TYPE_EDITOR, application.status.name)]

    def test_already_applied_for_manager(self, create_role_based_user, create_application_notification_obj):
        """Testcase: To test error when user has applied for manager role
        and try to apply for editor while manager application is not rejected yet."""

        consumer_user = create_role_based_user(name='consumer')
        application = create_application_notification_obj(
            user=consumer_user,
            notification_type=NOTIFICATION_TYPE_MANAGER_REQUEST
        )

        data = {
            'check': True,
        }

        form = EditorApplicationForm(data, request=Request(consumer_user))
        assert not form.is_valid()
        assert form['check'].errors == [ALREADY_APPLIED_FOR__ROLE % (USER_TYPE_MANAGER, application.status.name)]

    def test_valid_form(self, create_role_based_user):
        """Testcase: To test form is valid."""

        consumer_user = create_role_based_user(name='consumer')

        data = {
            'check': True,
        }

        form = EditorApplicationForm(data, request=Request(consumer_user))
        assert form.is_valid()
