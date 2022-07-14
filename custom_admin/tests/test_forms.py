import pytest
from custom_admin.forms import (
    CategoryForm, ManagersPostUpdateForm, RestoreConfirmationForm, DeleteConfirmationForm, ManagersUserUpdateForm,
    ManagersAddCommentForm, EditorsPostUpdateForm
)
from news_blog.models import Categorie


class TestCategoryForm(object):
    """Test Class for CategoryForm."""

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ('invalid_data', 'error'),
        [
            # Both Empty
            (
                    {'name': '', 'description': ''},
                    ('name', ["This field is required."])
            ),
            # Empty name
            (
                    {'name': '', 'description': 'This is test description'},
                    ('name', ["This field is required."])
            )
        ]
    )
    def test_category_form_errors(self, invalid_data, error):
        """Test Case: Category Form for invalid form-data."""

        form = CategoryForm(data=invalid_data)
        assert not form.is_valid()
        assert form.errors[error[0]] == error[1]

    @pytest.mark.django_db
    def test_name_already_exists(self, create_categorie_obj):
        """Test Case: This tests for name field is already existed."""

        obj = create_categorie_obj(name='sports')
        assert obj == Categorie.objects.first()

        data = {
            'name': 'sports',
            'description': ''
        }
        form = CategoryForm(data)
        assert not form.is_valid()
        assert form.errors['name'] == ['Categorie with this Name already exists.']

    @pytest.mark.django_db
    def test_update_name_already_exists(self, create_categorie_obj):
        """Test Case: This tests name field in update form if name already exists."""

        create_categorie_obj(name='sports')
        obj = create_categorie_obj(name='politics')

        data = {
            'name': 'sports',
            'description': '',
        }
        form = CategoryForm(data, instance=obj)
        assert not form.is_valid()
        assert form.errors['name'] == ['Categorie with this Name already exists.']

    @pytest.mark.django_db
    def test_valid_form(self, create_categorie_obj):
        """Test Case: This tests for valid form-data."""

        obj = create_categorie_obj(name='sports')
        assert obj == Categorie.objects.first()

        data = {
            'name': 'politics',
            'description': '',
        }
        form = CategoryForm(data, instance=obj)
        assert form.is_valid()

    @pytest.mark.django_db
    def test_name_field_lowercase(self, create_categorie_obj):
        """Test Case: This tests name field is in lower case."""

        data = {
            'name': 'SPORTS',
            'description': '',
        }
        form = CategoryForm(data)
        assert form.is_valid()
        assert form.cleaned_data.get('name') == 'sports'


class TestManagersPostUpdateForm(object):
    """Test Class for ManagersPostUpdateForm."""

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ('invalid_data', 'error'),
        [
            # Title Empty
            (
                    {
                        'title': ''
                    },
                    ('title', ["This field is required."])
            ),
            # Content Empty
            (
                    {
                        'content': ''
                    },
                    ('content', ["This field is required."])
            )
        ]
    )
    def test_manager_post_update_form_errors(self, invalid_data, error, create_post_obj):
        """Test Case: ManagersPostUpdate Form for invalid form-data."""

        obj = create_post_obj(
            title='Test Title',
            content='Test Content'
        )

        form = ManagersPostUpdateForm(data=invalid_data, instance=obj)
        assert not form.is_valid()
        assert form.errors[error[0]] == error[1]

    def test_valid_form(self, create_post_obj, create_post_status_obj, create_categorie_obj):
        """Test Case: This tests for valid form-data."""

        obj = create_post_obj(
            title='Test Title',
            content='Test Content'
        )
        sport = create_categorie_obj(name='sports')
        obj.category.add(sport)
        data = {
            'title': 'New Title Update',
            'content': 'New Content Update',
            'status': create_post_status_obj('active'),
            'category': Categorie.objects.all()
        }

        form = ManagersPostUpdateForm(data, instance=obj)

        assert form.is_valid()


class TestRestoreConfirmationForm(object):
    """Test Class for RestoreConfirmationForm."""

    @pytest.mark.django_db
    def test_uncheck(
            self,
            create_post_obj,
            create_post_status_obj,
            create_post_recycle_obj
    ):
        """Test Case:This tests for un-checked checkbox."""

        data = {
            'check': False
        }

        form = RestoreConfirmationForm(data)
        assert not form.is_valid()
        assert form['check'].errors == ['This field is required.']

    @pytest.mark.django_db
    def test_check(
            self,
            create_post_obj,
            create_post_status_obj,
            create_post_recycle_obj
    ):
        """Test Case:This tests for checked checkbox."""

        post = create_post_obj(
            title='Test Title',
            content='Test Content',
            status=create_post_status_obj('deleted'),
        )
        obj = create_post_recycle_obj(post=post)
        data = {
            'check': True
        }

        form = RestoreConfirmationForm(data, pk=obj.id)
        assert form.is_valid()

        form = RestoreConfirmationForm(data, pk=2)
        assert not form.is_valid()
        assert form['check'].errors == ['Invalid object id.']


class TestDeleteConfirmationForm(object):
    """Test Class for DeleteConfirmationForm."""

    def test_uncheck(self):
        """Test Case:This tests for un-checked checkbox."""

        data = {
            'check': False
        }

        form = DeleteConfirmationForm(data)
        assert not form.is_valid()
        assert form['check'].errors == ['This field is required.']

    def test_check(self, create_post_obj):
        """Test Case:This tests for checked checkbox."""

        post = create_post_obj(
            title='Test Title',
            content='Test Content',
        )

        data = {
            'check': True
        }

        form = DeleteConfirmationForm(data, pk=post.id)
        assert form.is_valid()

        form = DeleteConfirmationForm(data, pk=2)
        assert not form.is_valid()
        assert form['check'].errors == ['Invalid object id.']


class TestManagersUserUpdateForm(object):
    """Test Class for ManagersUserUpdateForm."""

    def test_valid_form(self, create_role_based_user):
        """Test Case: This tests for valid form-data."""

        user = create_role_based_user()
        data = {
            'email': user.email,
            'is_blocked': False
        }
        form = ManagersUserUpdateForm(data, instance=user)
        assert form.is_valid()

        data = {
            'email': user.email,
            'is_blocked': True
        }
        form = ManagersUserUpdateForm(data, instance=user)
        assert form.is_valid()


class TestManagersAddCommentForm(object):
    """Test Class for ManagersAddCommentForm."""

    def test_comment(self, create_role_based_user, create_post_obj):
        """Test Case: This tests comment field."""

        manager = create_role_based_user(name='manager')
        post = create_post_obj(
            title='Test title',
            content='Test content'
        )
        data = {
            'comment': ''
        }

        form = ManagersAddCommentForm(data, user=manager, pk=post.id)
        assert not form.is_valid()
        assert form['comment'].errors == ['This field is required.']

    def test_valid_form(self, create_role_based_user, create_post_obj):
        """Test Case: This tests for valid form-data."""

        manager = create_role_based_user(name='manager')
        post = create_post_obj(
            title='Test title',
            content='Test content'
        )
        data = {
            'comment': 'This is goo post.'
        }

        form = ManagersAddCommentForm(data, user=manager, pk=post.id)
        assert form.is_valid()


class TestEditorsPostUpdateForm(object):
    """Test Class for EditorsPostUpdateForm."""

    def test_valid_form(
            self,
            create_role_based_user,
            create_post_obj,
            create_post_status_obj,
            create_categorie_obj
    ):
        """Test Case: This tests for valid form-data."""

        editor = create_role_based_user(name='editor')
        post = create_post_obj(
            title='Test Title',
            content='Test Content',
            author=editor,
            status=create_post_status_obj('pending'),
        )
        create_categorie_obj(name='sports')
        data = {
            'title': 'Title Updated',
            'content': 'Content Updated',
            'category': Categorie.objects.all()
        }
        form = EditorsPostUpdateForm(data, instance=post)
        assert form.is_valid()

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ('invalid_data', 'error'),
        [
            # Title Empty
            (
                    {
                        'title': ''
                    },
                    ('title', ["This field is required."])
            ),
            # Content Empty
            (
                    {
                        'content': ''
                    },
                    ('content', ["This field is required."])
            ),
            # Category Empty
            (
                    {
                        'category': ''
                    },
                    ('category', ["This field is required."])
            )
        ]
    )
    def test_invalid_form(
            self,
            invalid_data,
            error,
            create_role_based_user,
            create_post_obj,
            create_post_status_obj,
            create_categorie_obj
    ):
        """Test Case: EditorsPostUpdate Form for invalid form-data."""

        editor = create_role_based_user(name='editor')
        post = create_post_obj(
            title='Test Title',
            content='Test Content',
            author=editor,
            status=create_post_status_obj('pending'),
        )
        create_categorie_obj(name='sports')
        form = EditorsPostUpdateForm(data=invalid_data, instance=post)

        assert not form.is_valid()
        assert form.errors[error[0]] == error[1]

