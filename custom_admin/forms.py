from django import forms
from users.models import CustomUser as User
from news_blog.models import Categorie
from django.core.exceptions import ValidationError


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








