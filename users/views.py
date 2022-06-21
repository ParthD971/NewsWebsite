from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .token import account_activation_token
from .models import CustomUser as User, UserType
from .mail import send_email
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import Group
from .constants import user_login_success, WRONG_CREDENTIALS, INVALID_INFORMATION, ALREADY_USER_EXISTS, VERIFY_EMAIL, \
    EMAIL_CONFIRMATION, INVALID_VERIFICATION_LINK, PASSWORD_RESET_INSTRUCTION


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(
            request=request,
            template_name="users/login.html",
            context={"login_form": form}
        )

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, user_login_success(user.email))
                return redirect("home")
            messages.error(request, WRONG_CREDENTIALS)
            return render(
                request=request,
                template_name="users/login.html",
                context={"login_form": form}
            )
        messages.error(request, WRONG_CREDENTIALS)
        return render(
            request=request,
            template_name="users/login.html",
            context={"login_form": form}
        )


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request=request, template_name="users/register.html", context={"register_form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.type = UserType.objects.get(name='consumer')
                user.save()
                messages.success(request, VERIFY_EMAIL)
            except UserType.DoesNotExist as e:
                messages.error(request, 'User type don\'t exists')
                return redirect("home")
        else:
            email = form.cleaned_data.get('email')
            query = None
            if email:
                query = User.objects.filter(email=email)
            if query and query.exists():
                to_email = email
                user = query.first()
                send_email(request, user, to_email)
            messages.error(request, INVALID_INFORMATION)
        return render(
            request=request,
            template_name="users/register.html",
            context={"register_form": form}
        )


def logout_request(request):
    logout(request)
    return redirect('home')


class ActivateEmail(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            my_group = Group.objects.get(name='Consumer')
            my_group.user_set.add(user)
            user.save()
            messages.success(request, EMAIL_CONFIRMATION)
            return redirect("home")
        messages.error(request, INVALID_VERIFICATION_LINK)
        return redirect("home")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = PASSWORD_RESET_INSTRUCTION
    success_url = reverse_lazy('home')
