from django import forms
from users.models import CustomUser as User
from news_blog.models import Categorie, Post, PostStatus, PostRecycle
from django.core.exceptions import ValidationError
from django.db.models import Q
from news_blog.constants import POST_TYPE_CHOICES
from .models import ManagerComment


class CategoryForm(forms.ModelForm):
    description = forms.CharField(required=False)

    def clean_name(self):
        return self.cleaned_data.get("name").lower()

    class Meta:
        model = Categorie
        fields = ['name', 'description']


class ManagersPostUpdateForm(forms.ModelForm):
    title = forms.CharField(max_length=200, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            # values = ['rejected', 'active', 'inreview', 'deleted', 'inactive', 'pending']
            query = None
            if self.instance.status.name == 'pending':
                # SCRAPED
                if self.instance.post_type == POST_TYPE_CHOICES[0][0]:
                    query = Q(name='active') | Q(name='inreview') | Q(name='deleted')
                # MANUAL
                else:
                    query = Q(name='active') | Q(name='inreview') | Q(name='rejected')
            elif self.instance.status.name == 'active':
                query = Q(name='inactive')
            elif self.instance.status.name == 'inreview':
                # SCRAPED
                if self.instance.post_type == POST_TYPE_CHOICES[0][0]:
                    query = Q(name='active') | Q(name='deleted')
                # MANUAL
                else:
                    query = Q(name='active') | Q(name='rejected')
            elif self.instance.status.name == 'inactive':
                # SCRAPED
                if self.instance.post_type == POST_TYPE_CHOICES[0][0]:
                    query = Q(name='active') | Q(name='deleted')
                # MANUAL
                else:
                    query = Q(name='active') | Q(name='rejected') | Q(name='deleted')
            self.fields['status'].queryset = PostStatus.objects.filter(query)

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'status', 'premium']


class RestoreConfirmationForm(forms.Form):
    check = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super().__init__(*args, **kwargs)

    def clean_check(self):
        if not PostRecycle.objects.filter(id=self.pk).exists():
            raise ValidationError('Invalid object id.')


class DeleteConfirmationForm(forms.Form):
    check = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super().__init__(*args, **kwargs)

    def clean_check(self):
        if not Post.objects.filter(id=self.pk).exists():
            raise ValidationError('Invalid object id.')


class ManagersUserUpdateForm(forms.ModelForm):
    age = forms.IntegerField(required=False)
    user_type = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(ManagersUserUpdateForm, self).__init__(*args, **kwargs)
        self.instance = getattr(self, 'instance', None)
        if self.instance and self.instance.pk:
            self.fields['first_name'].widget.attrs['readonly'] = True
            self.fields['last_name'].widget.attrs['readonly'] = True
            self.fields['age'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['user_type'].widget.attrs['disabled'] = True
            self.fields['is_premium_user'].widget.attrs['disabled'] = True
            self.initial['user_type'] = self.instance.user_type.name

    def clean_first_name(self):
        return self.instance.first_name

    def clean_last_name(self):
        return self.instance.last_name

    def clean_age(self):
        return self.instance.age

    def clean_email(self):
        return self.instance.email

    def clean_user_type(self):
        return self.instance.user_type

    def clean_is_premium_user(self):
        return self.instance.is_premium_user

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age', 'user_type', 'email', 'is_blocked', 'is_premium_user']


class ManagersAddCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        query = ManagerComment.objects.filter(manager=self.user, post_id=self.pk)
        if query.exists():
            obj = query.first()
            self.initial['comment'] = obj.comment

    class Meta:
        model = ManagerComment
        fields = ['comment']


class EditorsPostUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditorsPostUpdateForm, self).__init__(*args, **kwargs)
        self.instance = getattr(self, 'instance', None)
        if self.instance and self.instance.pk:
            obj = self.instance.status.name
            status = ['pending', 'rejected']
            if obj not in status:
                self.fields['title'].widget.attrs['readonly'] = True
                self.fields['content'].widget.attrs['readonly'] = True
                self.fields['category'].widget.attrs['disabled'] = True
                self.fields['image'].widget.attrs['disabled'] = True
                self.fields['premium'].widget.attrs['disabled'] = True

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'premium']

