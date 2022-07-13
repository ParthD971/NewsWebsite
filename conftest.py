import pytest
from django.contrib.auth.models import Group
from users.models import UserType
import uuid
from news_blog.models import ApplicationNotification, NotificationType, NotificationStatus, Post, PostStatus, Categorie, \
    PostRecycle, PostNotification, PostView, PostStatusRecord
from news_blog.constants import NOTIFICATION_STATUS_PENDING, NOTIFICATION_TYPE_EDITOR_REQUEST


@pytest.fixture
def create_user_type_obj(db, django_user_model):
    """ Fixture: creates user type based on argument."""

    def make_user_type(**kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = str(uuid.uuid4())
        return UserType.objects.get_or_create(name=kwargs['name'])[0]
    return make_user_type


@pytest.fixture
def create_group_obj(db, django_user_model):
    """ Fixture: creates group based on argument."""

    def make_group(**kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = str(uuid.uuid4())
        return Group.objects.get_or_create(name=kwargs['name'])[0]
    return make_group


@pytest.fixture
def create_groups(db, django_user_model, create_group_obj):
    """ Fixture: creates initial groups for role based authentication."""
    create_group_obj(name='consumer')
    create_group_obj(name='editor')
    create_group_obj(name='manager')
    create_group_obj(name='admin')


@pytest.fixture
def create_user_types(db, django_user_model, create_user_type_obj):
    """ Fixture: creates user types."""

    create_user_type_obj(name='consumer')
    create_user_type_obj(name='editor')
    create_user_type_obj(name='manager')
    create_user_type_obj(name='admin')


@pytest.fixture
def test_password():
    return 'StrongPass@2000'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    """Fixture: Creates normal user without user type consumer and group consumer."""

    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'email' not in kwargs:
            kwargs['email'] = str(uuid.uuid4()) + '@gmail.com'
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_role_based_user(db, create_groups, create_user_types, create_user, test_password):
    """Fixture: Creates user with user type and group given in argument.
    If no argument is provided then creates consumer type user.
    """

    def make_user(**kwargs):
        name = kwargs.pop('name', 'consumer')
        user = create_user(**kwargs)
        user.user_type = UserType.objects.get(name=name)
        grp = Group.objects.get(name=name)
        grp.user_set.add(user)
        user.save()
        return user

    return make_user


@pytest.fixture
def auto_login_consumer_user(db, client, create_role_based_user, test_password):
    """
    Fixture: Logs-in user which is passed as parameter.
    If user is None then it will create consumer user, then logs-in.
    It returns client and user.
    """

    def make_auto_login(user=None):
        if user is None:
            user = create_role_based_user(name='consumer')
        client.login(email=user.email, password=test_password)
        return client, user

    return make_auto_login


@pytest.fixture
def create_notification_type_obj(db):
    def make_obj(name=None):
        if name is None:
            name = str(uuid.uuid4())
        return NotificationType.objects.get_or_create(name=name)[0]

    return make_obj


@pytest.fixture
def create_notification_status_obj(db):
    def make_obj(name=None):
        if name is None:
            name = str(uuid.uuid4())
        notification_type = NotificationStatus.objects.get_or_create(name=name)[0]
        return notification_type
    return make_obj


@pytest.fixture
def create_application_notification_obj(db, create_role_based_user, create_notification_type_obj, create_notification_status_obj):
    def make_obj(user=None, status=None, notification_type=None):
        if user is None:
            user = create_role_based_user(name='consumer')

        if status is None:
            status = NOTIFICATION_STATUS_PENDING

        if notification_type is None:
            notification_type = NOTIFICATION_TYPE_EDITOR_REQUEST

        return ApplicationNotification.objects.get_or_create(
            user=user,
            notification_type=create_notification_type_obj(name=notification_type),
            status=create_notification_status_obj(name=status)
        )[0]

    return make_obj


@pytest.fixture
def test_content():
    return 'Content'


@pytest.fixture
def create_post_status_obj(db):
    def make_obj(name=None):
        if name is None:
            name = 'pending'
        return PostStatus.objects.get_or_create(name=name)[0]
    return make_obj


@pytest.fixture
def create_post_obj(db, create_role_based_user, test_content, create_post_status_obj):
    def make_obj(**kwargs):
        if kwargs.get('title', None) is None:
            kwargs['title'] = 'Title: ' + str(uuid.uuid4())

        if kwargs.get('author', None) is None:
            kwargs['author'] = create_role_based_user(name='editor')

        if kwargs.get('content', None) is None:
            kwargs['content'] = test_content

        if kwargs.get('status', None) is None:
            kwargs['status'] = create_post_status_obj(name='pending')

        if kwargs.get('author_display_name', None) is None:
            kwargs['author_display_name'] = kwargs['author'].first_name

        if kwargs.get('premium', None) is None:
            kwargs['premium'] = False

        return Post.objects.get_or_create(**kwargs)[0]

    return make_obj


@pytest.fixture(scope='module')
def get_data(request):
    return {
        'home': 'news_blog/home.html',
        'post-detail': 'news_blog/news_detail.html',
        # 'follow': 'news_blog/home.html',
        # 'notification-seen': 'news_blog/home.html',
        'notification-list': 'news_blog/post_notification_list.html',
        # 'add-views': 'news_blog/home.html',
        'apply-for-manager': 'news_blog/manager_application.html',
        'apply-for-editor': 'news_blog/editor_application.html',
        'apply-for-premium-user': 'news_blog/premium_user_application.html',
        'notification-from-admin': 'news_blog/notification_from_admin.html',
        # 'admin-notification-seen': 'news_blog/home.html',
    }


@pytest.fixture
def create_categorie_obj(db):
    """ Fixture: creates Categorie object based on argument."""

    def make_obj(**kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = str(uuid.uuid4())
        return Categorie.objects.get_or_create(name=kwargs['name'])[0]
    return make_obj


@pytest.fixture
def create_post_recycle_obj(db, create_role_based_user, create_post_obj, create_post_status_obj):
    def make_obj(**kwargs):
        if kwargs.get('deleted_by', None) is None:
            kwargs['deleted_by'] = create_role_based_user(name='editor')

        if kwargs.get('post', None) is None:
            kwargs['post'] = create_post_obj(
                author=kwargs['deleted_by'],
                status=create_post_status_obj(name='deleted')
            )

        return PostRecycle.objects.get_or_create(**kwargs)[0]

    return make_obj


@pytest.fixture
def create_post_notification_obj(db, create_role_based_user, create_post_obj, create_notification_type_obj):
    def make_obj(**kwargs):
        if kwargs.get('user', None) is None:
            kwargs['user'] = create_role_based_user(name='consumer')

        if kwargs.get('post', None) is None:
            kwargs['post'] = create_post_obj()

        if kwargs.get('notification_type', None) is None:
            kwargs['notification_type'] = create_notification_type_obj(name='created')

        return PostNotification.objects.get_or_create(**kwargs)[0]

    return make_obj


@pytest.fixture
def create_post_view_obj(db, create_role_based_user, create_post_obj):
    def make_obj(**kwargs):
        if kwargs.get('user', None) is None:
            kwargs['user'] = create_role_based_user(name='consumer')

        if kwargs.get('post', None) is None:
            kwargs['post'] = create_post_obj()

        return PostView.objects.get_or_create(**kwargs)[0]

    return make_obj


@pytest.fixture
def create_post_status_record_obj(db, create_role_based_user, create_post_obj, create_post_status_obj):
    def make_obj(**kwargs):
        if kwargs.get('changed_by', None) is None:
            kwargs['post'] = create_post_obj()
            kwargs['changed_by'] = kwargs['post'].author

        if kwargs.get('post', None) is None:
            kwargs['post'] = create_post_obj(author=kwargs['changed_by'])

        if kwargs.get('status', None) is None:
            kwargs['status'] = create_post_status_obj(name='pending')

        return PostStatusRecord.objects.get_or_create(**kwargs)[0]

    return make_obj




