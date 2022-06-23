from django import forms
from users.models import CustomUser as User
from news_blog.models import Categorie, Post, PostStatus
from django.core.exceptions import ValidationError
from django.db.models import Q


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
                query = Q(name='active') | Q(name='inreview') | Q(name='rejected')
            elif self.object.status.name == 'active':
                query = Q(name='inactive')
            elif self.object.status.name == 'inreview':
                query = Q(name='active') | Q(name='rejected')
            elif self.object.status.name == 'inactive':
                query = Q(name='active') | Q(name='rejected') | Q(name='deleted')
            self.fields['status'].queryset = PostStatus.objects.filter(query)

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'status']











