from django import forms
from users.models import CustomUser as User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"





