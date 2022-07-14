from django.shortcuts import render, redirect
from users.models import CustomUser as User, UserType
from django.views.generic import ListView, View
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import Group
from news_blog.models import (
    ApplicationNotification,
    Post,
    PostStatus,
    Categorie,
    PostNotification,
    Follow,
    NotificationType,
    PostRecycle,
    PostStatusRecord,
    NotificationStatus,
    PCMiddle,
    PostView
)
from django.db.models import Q
from news_blog.paginators import CustomPaginator
from custom_admin.models import ManagerComment, AdminNotification
from news_blog.permissions import GroupRequiredMixin
from news_blog.helpers import get_paginated_context


class AdminMainPageView(GroupRequiredMixin, View):
    group_required = [u'admin']

    def get(self, request):
        return render(
            request=request,
            template_name="custom_admin/admin_main_page.html",
            context={}
        )


class AdminUserListView(GroupRequiredMixin, ListView):
    model = User
    template_name = 'users/admin_user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    paginator_class = CustomPaginator
    group_required = [u'admin']
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        context['user_types'] = UserType.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_superuser=False)

        search = self.request.GET.get('search', '')
        if search.strip():
            return queryset.filter(Q(first_name__contains=search) | Q(last_name__contains=search))

        blocked = self.request.GET.get('blocked', '')
        if blocked:
            queryset = queryset.filter(is_blocked=blocked == 'True')

        staff = self.request.GET.get('staff', '')
        if staff:
            queryset = queryset.filter(is_staff=staff == 'True')

        premium_user = self.request.GET.get('premium_user', '')
        if premium_user:
            queryset = queryset.filter(is_premium_user=premium_user == 'True')

        active = self.request.GET.get('active', '')
        if active:
            queryset = queryset.filter(is_active=active == 'True')

        user_type = self.request.GET.get('user_type', '')
        if user_type:
            queryset = queryset.filter(user_type__name=user_type)

        return queryset


class AdminUserUpdateView(GroupRequiredMixin, UpdateView):
    model = User
    fields = ['is_blocked']
    success_url = reverse_lazy('admin-user-list')
    template_name = 'users/admin_user_update.html'
    group_required = [u'admin']


class AdminApplicationNotificationListView(GroupRequiredMixin, ListView):
    model = ApplicationNotification
    template_name = 'users/admin_application_notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(status__name='pending')

        search = self.request.GET.get('search', '')
        if search.strip():
            return queryset.filter(Q(user__first_name__contains=search) | Q(user__last_name__contains=search))

        request_for = self.request.GET.get('request_for', '')
        if request_for:
            notification_type = 'manager request' if request_for == 'manager' else 'editor request'
            queryset = queryset.filter(notification_type__name=notification_type)

        return queryset


class AdminApplicationNotificationUpdateView(GroupRequiredMixin, UpdateView):
    model = ApplicationNotification
    fields = ['status']
    success_url = reverse_lazy('admin-application-notification-list')
    template_name = 'users/admin_application_update.html'
    group_required = [u'admin']

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
        return super(AdminApplicationNotificationUpdateView, self).form_valid(form)


class AdminCategorieListView(GroupRequiredMixin, ListView):
    model = Categorie
    template_name = 'news_blog/admin_categorie_list.html'
    context_object_name = 'categories'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context


class AdminFollowListView(GroupRequiredMixin, ListView):
    model = Follow
    template_name = 'news_blog/admin_follow_list.html'
    context_object_name = 'follows'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context


class AdminNotificationStatusListView(GroupRequiredMixin, ListView):
    model = NotificationStatus
    template_name = 'news_blog/admin_notification_status_list.html'
    context_object_name = 'notification_statuses'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context


class AdminNotificationTypeListView(GroupRequiredMixin, ListView):
    model = NotificationType
    template_name = 'news_blog/admin_notification_type_list.html'
    context_object_name = 'notification_types'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context


class AdminPCMiddleListView(GroupRequiredMixin, ListView):
    model = PCMiddle
    template_name = 'news_blog/admin_pcmiddle_list.html'
    context_object_name = 'pcmiddles'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context


class AdminPostNotificationListView(GroupRequiredMixin, ListView):
    model = PostNotification
    template_name = 'news_blog/admin_post_notification_list.html'
    context_object_name = 'post_notifications'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context


class AdminPostRecycleListView(GroupRequiredMixin, ListView):
    model = PostRecycle
    template_name = 'news_blog/admin_post_recycle_list.html'
    context_object_name = 'post_recycles'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context


class AdminPostStatusRecordListView(GroupRequiredMixin, ListView):
    model = PostStatusRecord
    template_name = 'news_blog/admin_post_status_record_list.html'
    context_object_name = 'post_status_records'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context


class AdminPostStatusListView(GroupRequiredMixin, ListView):
    model = PostStatus
    template_name = 'news_blog/admin_post_status_list.html'
    context_object_name = 'post_statuses'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context


class AdminPostViewsListView(GroupRequiredMixin, ListView):
    model = PostView
    template_name = 'news_blog/admin_post_view_list.html'
    context_object_name = 'post_views'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context


class AdminPostListView(GroupRequiredMixin, ListView):
    model = Post
    template_name = 'news_blog/admin_post_list.html'
    context_object_name = 'posts'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context


class AdminUserTypeListView(GroupRequiredMixin, ListView):
    model = UserType
    template_name = 'users/admin_user_type_list.html'
    context_object_name = 'user_types'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context


class AdminManagerCommentListView(GroupRequiredMixin, ListView):
    model = ManagerComment
    template_name = 'custom_admin/admin_manager_comment_list.html'
    context_object_name = 'manager_comments'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context


class AdminNotificationListView(GroupRequiredMixin, ListView):
    model = AdminNotification
    template_name = 'custom_admin/admin_notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['-id']
    group_required = [u'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        return context


class AdminSendNotificationView(GroupRequiredMixin, View):
    group_required = [u'admin']

    def get(self, request):
        context = {
            'users': User.objects.all().exclude(id=request.user.id)
        }
        return render(
            request,
            template_name='custom_admin/admin_send_notification.html',
            context=context
        )

    def post(self, request):
        send_to_user_ids = [int(user_id) for user_id in request.POST.getlist('checks[]')]
        message = request.POST.get('message').strip()
        error = False
        context = {}
        if not message:
            context['message_error'] = 'Message cannot be empty.'
            error = True
        if not send_to_user_ids:
            context['users_error'] = 'Must select at-lease one user.'
            error = True

        if error:
            context['users'] = User.objects.all().exclude(id=request.user.id)
            return render(
                request,
                template_name='custom_admin/admin_send_notification.html',
                context=context
            )

        notifications = [AdminNotification(receiver_id=user_id, message=message) for user_id in send_to_user_ids]
        AdminNotification.objects.bulk_create(notifications)

        messages.success(request, 'Message sent successfully.')
        return redirect('admin-panel')
