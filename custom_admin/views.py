from django.shortcuts import render, redirect
from users.models import CustomUser as User, UserType
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import Group
from news_blog.models import ApplicationNotification, NotificationStatus


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
    fields = ['user_type']
    success_url = reverse_lazy('users_table')
    template_name = 'users/user_update_form.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user_list = User.objects.filter(id=pk)
        if pk and user_list.exists():
            user = user_list.first()
            if user.is_superuser:
                return HttpResponse('You Are not Allowed this page')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.groups.clear()
        my_group = Group.objects.get(name=instance.user_type.name)
        my_group.user_set.add(instance)
        return super(UserUpdateView, self).form_valid(form)


class ApplicationNotificationListView(ListView):
    model = ApplicationNotification
    template_name = 'custom_admin/application_notification_table.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return ApplicationNotification.objects.filter(status__name='pending')


class ApplicationNotificationUpdateView(UpdateView):
    model = ApplicationNotification
    fields = ['status']
    success_url = reverse_lazy('application_notification_table')
    template_name = 'users/application_update_form.html'

    def form_valid(self, form):
        application_notification = form.save(commit=False)
        if application_notification.status.name == 'accepted':
            user = application_notification.user
            notification_type = application_notification.notification_type.name
            mapper = {
                'editor request': 'editor',
                'manager request': 'manager'
            }
            user.groups.clear()
            my_group = Group.objects.get(name=mapper[notification_type])
            my_group.user_set.add(user)
            user.user_type = UserType.objects.get(name=mapper[notification_type])
            user.is_staff = True
            user.save()
        return super(ApplicationNotificationUpdateView, self).form_valid(form)
