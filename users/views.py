from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .token import account_activation_token
from .models import CustomUser as User
from .mail import send_email
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


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
                messages.info(request, f"You are now logged in as {email}.")
                return redirect("home")
            messages.error(request, "Invalid username or password.")
            return render(
                request=request,
                template_name="users/login.html",
                context={"login_form": form}
            )
        messages.error(request, "Invalid username or password.")
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
            print('its valid')
            user = form.save(commit=False)
            print('after saving')
            user.is_active = False
            user.save()

            to_email = form.cleaned_data.get('email')
            send_email(request, user, to_email)

            messages.success(request, "Registration successful.")
            return redirect("home")
        if 'User with this Email address already exists.' in form.errors['email'][:][0]:
            to_email = request.POST.get('email')
            user = User.objects.get(email=to_email)
            send_email(request, user, to_email)
            messages.error(request, "Email is Already registered, Please verify email.")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
        return render(request=request, template_name="users/register.html", context={"register_form": form})


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
            user.first_name = user.email.split('@')[0]
            user.save()
            messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
            return redirect("home")
        messages.success(request, "Activation link is invalid!")
        return redirect("home")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')
