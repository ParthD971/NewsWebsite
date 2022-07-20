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
    is_blocked = forms.BooleanField(label='Block User', required=False)

    class Meta:
        model = User
        fields = ['is_blocked']


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

