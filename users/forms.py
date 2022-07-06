from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser as User
from validate_email_address import validate_email
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100,
        required=True,
        help_text='Enter Email Address',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    password1 = forms.CharField(
        help_text='Enter Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        required=True,
        help_text='Enter Password Again',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError('The two password fields didn\'t match.')

        return password2

    def clean_email(self):
        cleaned_data = self.clean()
        email = cleaned_data.get('email')

        if not validate_email(email, verify=True):
            raise ValidationError('Email not valid.')

        user = User.objects.filter(email=email)
        if user.exists() and user.first().is_blocked:
            raise ValidationError('Email is Blocked.')

        if user.exists() and not user.first().is_active:
            raise ValidationError('User with this Email address already register. We have sent verification mail. '
                                  'Please verify email.')

        return email

    class Meta:
        model = User
        fields = [
            'email', 'password1', 'password2',
        ]


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        required=True,
        help_text='Enter Email Address',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    password = forms.CharField(
        required=True,
        help_text='Enter Password Again',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
    )

    def clean_email(self):
        cleaned_data = self.clean()
        email = cleaned_data.get('email')

        user = User.objects.filter(email=email)
        if not user.exists():
            raise ValidationError('Email is not registered.')

        if user.exists() and user.first().is_blocked:
            raise ValidationError('Email is Blocked.')

        return email

    class Meta:
        model = User
        fields = [
            'email', 'password',
        ]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    def clean_age(self):
        cleaned_data = self.clean()
        age = cleaned_data.get('age')

        if age < 1 or age > 100:
            raise ValidationError("Age not valid")

        return age

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age']



        
