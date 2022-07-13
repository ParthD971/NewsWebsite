import pytest

from news_blog.constants import DEFAULT_IMAGE_PATH
from news_blog.models import PCMiddle


class TestCategorieModel(object):
    """Test Class for Categorie model."""

    @pytest.mark.django_db
    def test_name_lower_case(self, create_categorie_obj):
        """Testcase: This testcase tests that instance of
        Categorie will always save name attribute in lowercase."""

        category = create_categorie_obj(name='CAPITAL')
        assert category.name == 'capital'

    @pytest.mark.django_db
    def test_name(self, create_categorie_obj):
        """Testcase: This testcase tests name attribute value."""

        category = create_categorie_obj(name='sports')
        assert category.name == 'sports'

    @pytest.mark.django_db
    def test_string(self, create_categorie_obj):
        """Testcase: This testcase tests string method of Categorie Model Class."""

        category = create_categorie_obj(name='test')
        assert str(category) == 'test'

    @pytest.mark.django_db
    def test_max_length(self, create_categorie_obj):
        """Testcase: This testcase tests max_length parameter of name attribute."""

        category = create_categorie_obj(name='test')
        max_length = category._meta.get_field('name').max_length
        assert max_length == 50


class TestPostStatusModel(object):
    """Test Class for PostStatus model."""

    @pytest.mark.django_db
    def test_name_lower_case(self, create_post_status_obj):
        """Testcase: This testcase tests that instance of
        PostStatus will always save name attribute in lowercase."""

        obj = create_post_status_obj(name='CAPITAL')
        assert obj.name == 'capital'

    @pytest.mark.django_db
    def test_name(self, create_post_status_obj):
        """Testcase: This testcase tests name attribute value."""

        obj = create_post_status_obj(name='pending')
        assert obj.name == 'pending'

    @pytest.mark.django_db
    def test_string(self, create_post_status_obj):
        """Testcase: This testcase tests string method of PostStatus Model Class."""

        obj = create_post_status_obj(name='test')
        assert str(obj) == 'test'

    @pytest.mark.django_db
    def test_max_length(self, create_post_status_obj):
        """Testcase: This testcase tests max_length parameter of name attribute."""

        obj = create_post_status_obj(name='test')
        max_length = obj._meta.get_field('name').max_length
        assert max_length == 20


class TestNotificationTypeModel(object):
    """Test Class for NotificationType model."""

    @pytest.mark.django_db
    def test_name_lower_case(self, create_notification_type_obj):
        """Testcase: This testcase tests that instance of
        NotificationType will always save name attribute in lowercase."""

        obj = create_notification_type_obj(name='CAPITAL')
        assert obj.name == 'capital'

    @pytest.mark.django_db
    def test_name(self, create_notification_type_obj):
        """Testcase: This testcase tests name attribute value."""

        obj = create_notification_type_obj(name='pending')
        assert obj.name == 'pending'

    @pytest.mark.django_db
    def test_string(self, create_notification_type_obj):
        """Testcase: This testcase tests string method of NotificationType Model Class."""

        obj = create_notification_type_obj(name='test')
        assert str(obj) == 'test'

    @pytest.mark.django_db
    def test_max_length(self, create_notification_type_obj):
        """Testcase: This testcase tests max_length parameter of name attribute."""

        obj = create_notification_type_obj(name='test')
        max_length = obj._meta.get_field('name').max_length
        assert max_length == 50


class TestNotificationStatusModel(object):
    """Test Class for NotificationStatus model."""

    @pytest.mark.django_db
    def test_name_lower_case(self, create_notification_status_obj):
        """Testcase: This testcase tests that instance of
        NotificationStatus will always save name attribute in lowercase."""

        obj = create_notification_status_obj(name='CAPITAL')
        assert obj.name == 'capital'

    @pytest.mark.django_db
    def test_name(self, create_notification_status_obj):
        """Testcase: This testcase tests name attribute value."""

        obj = create_notification_status_obj(name='pending')
        assert obj.name == 'pending'

    @pytest.mark.django_db
    def test_string(self, create_notification_status_obj):
        """Testcase: This testcase tests string method of NotificationStatus Model Class."""

        obj = create_notification_status_obj(name='test')
        assert str(obj) == 'test'

    @pytest.mark.django_db
    def test_max_length(self, create_notification_status_obj):
        """Testcase: This testcase tests max_length parameter of name attribute."""

        obj = create_notification_status_obj(name='test')
        max_length = obj._meta.get_field('name').max_length
        assert max_length == 20


class TestPostModel(object):
    """Test Class for Post model."""

    @pytest.mark.django_db
    def test_string(self, create_post_obj, create_role_based_user, create_post_status_obj):
        """Testcase: This testcase tests string method of Post Model Class."""

        author = create_role_based_user(name='editor', email='desaiparth@gmail.com')
        title = 'Test Title'
        status = create_post_status_obj(name='pending')
        obj = create_post_obj(
            title=title,
            author=author,
            content='Test Content',
            status=status,
            author_display_name='Display Name'
        )
        assert str(obj) == ' | '.join([str(author), str(title), str(status)])

    @pytest.mark.django_db
    def test_max_length(self, create_post_obj, create_role_based_user, create_post_status_obj):
        """Testcase: This testcase tests max_length parameter of title and post_type attribute."""

        author = create_role_based_user(name='editor', email='desaiparth@gmail.com')
        title = 'Test Title'
        status = create_post_status_obj(name='pending')
        obj = create_post_obj(
            title=title,
            author=author,
            content='Test Content',
            status=status,
            author_display_name='Display Name'
        )
        max_length = obj._meta.get_field('title').max_length
        assert max_length == 200
        max_length = obj._meta.get_field('post_type').max_length
        assert max_length == 20

    @pytest.mark.django_db
    def test_defaults(self, create_post_obj, create_role_based_user, create_post_status_obj):
        """Testcase: This testcase tests default values of views, image and premium attribute."""

        author = create_role_based_user(name='editor', email='desaiparth@gmail.com')
        title = 'Test Title'
        status = create_post_status_obj(name='pending')
        obj = create_post_obj(
            title=title,
            author=author,
            content='Test Content',
            status=status,
            author_display_name='Display Name'
        )
        assert obj.views == 0
        assert obj.image == DEFAULT_IMAGE_PATH
        assert not obj.premium

    @pytest.mark.django_db
    def test_field_values(self, create_post_obj, create_role_based_user, create_post_status_obj):
        """Testcase: This testcase tests field values."""

        author = create_role_based_user(name='editor', email='desaiparth@gmail.com')
        title = 'Test Title'
        status = create_post_status_obj(name='pending')
        obj = create_post_obj(
            title=title,
            author=author,
            content='Test Content',
            status=status,
            author_display_name='Display Name'
        )
        assert obj.author == author
        assert obj.title == title
        assert obj.content == 'Test Content'
        assert obj.author_display_name == 'Display Name'
        assert obj.status == status
        assert obj.views == 0
        assert obj.image == DEFAULT_IMAGE_PATH
        assert not obj.premium


class TestPCMiddleModel(object):
    """Test Class for PCMiddle model."""

    @pytest.mark.django_db
    def test_table(self, create_post_obj, create_categorie_obj):
        post = create_post_obj(
            title='Test Title',
            content='Test Content',
            author_display_name='Display Name'
        )
        sports = create_categorie_obj(name='sports')
        entertainments = create_categorie_obj(name='entertainments')
        post.category.add(entertainments)
        post.category.add(sports)

        assert PCMiddle.objects.all().count() == 2


class TestPostRecycleModel(object):
    """Test Class for PostRecycle model."""

    @pytest.mark.django_db
    def test_string(self, create_post_status_obj, create_post_obj, create_post_recycle_obj):
        """Testcase: This testcase tests string method of PostRecycle Model Class."""

        status = create_post_status_obj(name='deleted')
        post = create_post_obj(
            title='Test Title',
            content='Test Content',
            status=status,
            author_display_name='Display Name'
        )
        deleted_by = post.author
        obj = create_post_recycle_obj(post=post, deleted_by=deleted_by)
        assert str(obj) == post.title

    @pytest.mark.django_db
    def test_field_values(self, create_post_status_obj, create_post_obj, create_post_recycle_obj):
        """Testcase: This testcase tests field values."""

        status = create_post_status_obj(name='deleted')
        post = create_post_obj(
            title='Test Title',
            content='Test Content',
            status=status,
            author_display_name='Display Name'
        )
        deleted_by = post.author
        obj = create_post_recycle_obj(post=post, deleted_by=deleted_by)
        assert obj.deleted_by == deleted_by
        assert obj.post == post


class TestPostNotificationModel(object):
    """Test Class for PostNotification model."""

    @pytest.mark.django_db
    def test_string(
            self,
            create_role_based_user,
            create_notification_type_obj,
            create_post_status_obj,
            create_post_obj,
            create_post_notification_obj
    ):
        """Testcase: This testcase tests string method of PostNotification Model Class."""

        status = create_post_status_obj(name='pending')
        post = create_post_obj(
            title='Test Title',
            content='Test Content',
            status=status,
            author_display_name='Display Name'
        )
        notification_type = create_notification_type_obj(name='created')
        user = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        obj = create_post_notification_obj(post=post, user=user, notification_type=notification_type)
        assert str(obj) == ' -> '.join([str(post), user.first_name])

    @pytest.mark.django_db
    def test_field_values(
            self,
            create_role_based_user,
            create_notification_type_obj,
            create_post_status_obj,
            create_post_obj,
            create_post_notification_obj
    ):
        """Testcase: This testcase tests field values."""

        status = create_post_status_obj(name='pending')
        post = create_post_obj(
            title='Test Title',
            content='Test Content',
            status=status,
            author_display_name='Display Name'
        )
        notification_type = create_notification_type_obj(name='created')
        user = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        obj = create_post_notification_obj(post=post, user=user, notification_type=notification_type)
        assert obj.post == post
        assert obj.user == user
        assert not obj.seen
        assert obj.notification_type == notification_type


class TestApplicationNotificationModel(object):
    """Test Class for ApplicationNotification model."""

    @pytest.mark.django_db
    def test_string(
            self,
            create_application_notification_obj,
            create_role_based_user,
            create_notification_type_obj,
            create_notification_status_obj
    ):
        """Testcase: This testcase tests string method of ApplicationNotification Model Class."""

        user = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        notification_type = create_notification_type_obj(name='manager request')
        notification_status = create_notification_status_obj(name='pending')

        obj = create_application_notification_obj(
            user=user,
            status=notification_status,
            notification_type=notification_type
        )

        assert str(obj) == ' | '.join([user.first_name, notification_status.name, notification_type.name])

    @pytest.mark.django_db
    def test_field_values(
            self,
            create_application_notification_obj,
            create_role_based_user,
            create_notification_type_obj,
            create_notification_status_obj
    ):
        """Testcase: This testcase tests field values."""

        user = create_role_based_user(name='consumer', email='desaiparth@gmail.com')
        notification_type = create_notification_type_obj(name='manager request')
        notification_status = create_notification_status_obj(name='pending')

        obj = create_application_notification_obj(
            user=user,
            status=notification_status,
            notification_type=notification_type
        )
        assert obj.user == user
        assert obj.status == notification_status
        assert obj.notification_type == notification_type


class TestPostViewModel(object):
    """Test Class for PostView model."""

    @pytest.mark.django_db
    def test_field_values(
            self,
            create_post_status_obj,
            create_post_obj,
            create_role_based_user,
            create_post_view_obj
    ):
        """Testcase: This testcase tests field values."""

        status = create_post_status_obj(name='pending')
        post = create_post_obj(
            title='Test Title',
            content='Test Content',
            status=status,
            author_display_name='Display Name'
        )
        user = create_role_based_user(name='consumer', email='desaiparth@gmail.com')

        obj = create_post_view_obj(user=user, post=post)
        assert obj.post == post
        assert obj.user == user


class TestPostStatusRecordModel(object):
    """Test Class for PostStatusRecord model."""

    @pytest.mark.django_db
    def test_string(
            self,
            create_post_status_obj,
            create_post_obj,
            create_role_based_user,
            create_post_status_record_obj
    ):
        """Testcase: This testcase tests string method of TestPostStatusRecordModel Model Class."""

        post = create_post_obj(
            title='Test Title',
            content='Test Content',
            status=create_post_status_obj(name='pending')
        )
        user = create_role_based_user(name='editor', email='desaiparth@gmail.com')
        obj = create_post_status_record_obj(changed_by=user, post=post, status=post.status)

        assert str(obj) == ' | '.join([user.first_name, post.status.name])

    @pytest.mark.django_db
    def test_field_values(
            self,
            create_post_status_obj,
            create_post_obj,
            create_role_based_user,
            create_post_status_record_obj
    ):
        """Testcase: This testcase tests field values."""

        post = create_post_obj(
            title='Test Title',
            content='Test Content',
            status=create_post_status_obj(name='pending')
        )
        user = create_role_based_user(name='editor', email='desaiparth@gmail.com')
        obj = create_post_status_record_obj(changed_by=user, post=post, status=post.status)

        assert obj.post == post
        assert obj.changed_by == user
        assert obj.status == post.status

        post.status = create_post_status_obj(name='active')
        post.save()
        obj = create_post_status_record_obj(changed_by=user, post=post, status=post.status)
        assert obj.status == post.status
