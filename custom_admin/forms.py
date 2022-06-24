from django import forms
from users.models import CustomUser as User
from news_blog.models import Categorie, Post, PostStatus, PostRecycle
from django.core.exceptions import ValidationError
from django.db.models import Q
from news_blog.constants import POST_TYPE_CHOICES


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.object = kwargs.pop('object', None)
        super(CategoryForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        name = name.lower()
        if self.object and Categorie.objects.exclude(id=self.object.id).filter(name=name).exists():
            raise ValidationError('Category already exists.')
        if self.object is None and Categorie.objects.filter(name=name).exists():
            raise ValidationError('Category already exists.')
        return name

    class Meta:
        model = Categorie
        fields = ['name']


class ManagersPostUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.object = kwargs.pop('object', None)
        super().__init__(*args, **kwargs)

        if hasattr(self, "instance") and self.instance:
            # values = ['rejected', 'active', 'inreview', 'deleted', 'inactive', 'pending']
            query = None
            if self.object.status.name == 'pending':
                # SCRAPED
                if self.object.post_type == POST_TYPE_CHOICES[0][0]:
                    query = Q(name='active') | Q(name='inreview') | Q(name='deleted')
                # MANUAL
                else:
                    query = Q(name='active') | Q(name='inreview') | Q(name='rejected')
            elif self.object.status.name == 'active':
                query = Q(name='inactive')
            elif self.object.status.name == 'inreview':
                # SCRAPED
                if self.object.post_type == POST_TYPE_CHOICES[0][0]:
                    query = Q(name='active') | Q(name='deleted')
                # MANUAL
                else:
                    query = Q(name='active') | Q(name='rejected')
            elif self.object.status.name == 'inactive':
                # SCRAPED
                if self.object.post_type == POST_TYPE_CHOICES[0][0]:
                    query = Q(name='active') | Q(name='deleted')
                # MANUAL
                else:
                    query = Q(name='active') | Q(name='rejected') | Q(name='deleted')
            self.fields['status'].queryset = PostStatus.objects.filter(query)

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'status']


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


