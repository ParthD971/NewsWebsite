from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .token import account_activation_token
from .models import CustomUser as User
from .mail import send_email


def login_request(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {email}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
                return render(request=request, template_name="users/login.html", context={"login_form": form})
        else:
            messages.error(request, "Invalid username or password.")
            return render(request=request, template_name="users/login.html", context={"login_form": form})
    form = LoginForm()
    return render(request=request, template_name="users/login.html", context={"login_form": form})


def register_request(request):
    if request.method == "POST":
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
        else:
            if 'User with this Email address already exists.' in form.errors['email'][:][0]:
                to_email = request.POST.get('email')
                user = User.objects.get(email=to_email)
                send_email(request, user, to_email)
                messages.error(request, "Email is Already registered, Please verify email.")
            else:
                messages.error(request, "Unsuccessful registration. Invalid information.")
            return render(request=request, template_name="users/register.html", context={"register_form": form})
    form = RegisterForm()
    return render(request=request, template_name="users/register.html", context={"register_form": form})


def logout_request(request):
    logout(request)
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect("home")

    else:
        messages.success(request, "Activation link is invalid!")
        return redirect("home")
