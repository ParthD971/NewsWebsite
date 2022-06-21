from django.shortcuts import render, redirect
from users.models import CustomUser as User
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from .forms import UserForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse


# login required and must be admin superuser
class AdminPanel(View):
    def get(self, request):
        return render(
            request=request,
            template_name="custom_admin/admin_panel.html",
            context={}
        )


class UsersListView(ListView):
    model = User
    template_name = 'custom_admin/users_table.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)


class UserUpdateView(UpdateView):
    model = User
    fields = ['type']
    success_url = reverse_lazy('users_table')

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user_list = User.objects.filter(id=pk)
        if pk and user_list.exists():
            user = user_list.first()
            if user.is_superuser:
                return HttpResponse('You Are not Allowed this page')
        return super().get(request, *args, **kwargs)



class UserDeleteView(DeleteView):
    model = User
    fields = "__all__"
    success_url = reverse_lazy('users_table')

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user_list = User.objects.filter(id=pk)
        if pk and user_list.exists():
            user = user_list.first()
            if user.is_superuser:
                return HttpResponse('You Are not Allowed this page')
        return super().get(request, *args, **kwargs)