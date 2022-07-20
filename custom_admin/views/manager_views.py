from django.shortcuts import render
from users.models import CustomUser as User, UserType
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from news_blog.models import (
    Post,
    PostStatus,
    Categorie,
    PostNotification,
    Follow,
    NotificationType,
    PostRecycle,
    PostStatusRecord,
)
from django.db.models import Q
from news_blog.paginators import CustomPaginator
from custom_admin.forms import (
    CategoryForm,
    ManagersPostUpdateForm,
    RestoreConfirmationForm,
    ManagersUserUpdateForm,
    ManagersAddCommentForm,
)
from custom_admin.models import ManagerComment
from news_blog.permissions import GroupRequiredMixin
from news_blog.helpers import get_paginated_context
from custom_admin.helpers import (
    get_queryset_for_created_on,
    get_queryset_for_categories,
    remove_and_update_image_for_post,
    get_queryset_for_deleted_on,
    get_queryset_for_search
)


class ManagerMainPageView(GroupRequiredMixin, View):
    group_required = [u'manager']

    def get(self, request):
        return render(
            request=request,
            template_name="custom_admin/manager_home_page.html",
            context={}
        )


class ManagerPostListView(GroupRequiredMixin, ListView):
    model = Post
    template_name = 'news_blog/manager_post_list.html'
    context_object_name = 'posts'
    paginate_by = 20
    ordering = ['-created_on', '-id']
    paginator_class = CustomPaginator
    group_required = [u'manager']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        # context for filters
        context['categories'] = Categorie.objects.all()
        context['statuses'] = PostStatus.objects.all().exclude(Q(name='rejected') | Q(name='deleted'))
        context['authors'] = Post.objects.order_by('author_display_name').values(
            'author_display_name').distinct()

        return context

    def get_queryset(self):
        queryset = super().get_queryset().exclude(Q(status__name='rejected') | Q(status__name='deleted'))
        search = self.request.GET.get('search', '')

        status = self.request.GET.get('status', '').strip()
        editor_display_name = self.request.GET.get('editor', '').strip()

        queryset = get_queryset_for_created_on(
            request=self.request,
            queryset=queryset
        )

        queryset = get_queryset_for_categories(
            request=self.request,
            queryset=queryset,
            categories=Categorie.objects.all()
        )

        if status:
            queryset = queryset.filter(status__name=status)

        if editor_display_name:
            queryset = queryset.filter(author_display_name=editor_display_name)

        if search:
            queryset = queryset.filter(Q(title__contains=search) | Q(content__contains=search))
        return queryset


class ManagerPostUpdateView(GroupRequiredMixin, UpdateView):
    model = Post
    form_class = ManagersPostUpdateForm
    success_url = reverse_lazy('manager-post-list')
    template_name = 'news_blog/manager_editor_post_update.html'
    group_required = [u'manager']

    def form_valid(self, form):
        post_obj = form.instance

        # if update status
        old_status = Post.objects.get(id=post_obj.id).status.name
        new_status = post_obj.status.name

        status_changed = old_status != new_status

        if status_changed:
            if new_status == 'active':
                if old_status == 'pending' or old_status == 'inreview' or old_status == 'inactive':
                    # sending notifications
                    new_post_obj = Post.objects.get(id=post_obj.id)
                    followers = Follow.objects.select_related('user').filter(author=new_post_obj.author)
                    notification_type = NotificationType.objects.get(name='post added')
                    post_notifications = [
                        PostNotification(
                            post=new_post_obj,
                            user=follower.user,
                            notification_type=notification_type
                        ) for follower in followers
                    ]
                    PostNotification.objects.bulk_create(post_notifications)
            elif new_status == 'inactive':
                if old_status == 'active':
                    new_post_obj = Post.objects.get(id=post_obj.id)
                    followers = Follow.objects.select_related('user').filter(author=new_post_obj.author)
                    print(followers)
                    notification_type = NotificationType.objects.get(name='post deleted')
                    post_notifications = [
                        PostNotification(
                            post=new_post_obj,
                            user=follower.user,
                            notification_type=notification_type
                        ) for follower in followers
                    ]
                    PostNotification.objects.bulk_create(post_notifications)
            elif new_status == 'deleted':
                # inactive -> deleted then move to Recycle Table
                if old_status == 'inactive':
                    post_recycle_obj = PostRecycle(
                        post=post_obj,
                        deleted_by=self.request.user
                    )
                    post_recycle_obj.save()
            elif new_status == 'inreview':
                if old_status == 'pending':
                    # nothing to do
                    pass
            elif new_status == 'rejected':
                if old_status == 'pending':
                    pass

            # if status changed then update record
            PostStatusRecord(
                changed_by=self.request.user,
                post=post_obj,
                status=post_obj.status
            ).save()

        # if image is updated then remove old image
        if 'image' in form.changed_data:
            remove_and_update_image_for_post(old_post_obj=Post.objects.get(id=post_obj.id))

        return super(ManagerPostUpdateView, self).form_valid(form)


class ManagerCategorieListView(GroupRequiredMixin, ListView):
    model = Categorie
    template_name = 'news_blog/manager_categorie_list.html'
    context_object_name = 'categories'
    group_required = [u'manager']

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search.strip():
            return queryset.filter(Q(name__contains=search))
        return queryset


class ManagerCategorieCreateView(GroupRequiredMixin, CreateView):
    model = Categorie
    template_name = 'news_blog/manager_categorie_create.html'
    success_url = reverse_lazy('manager-categorie-list')
    form_class = CategoryForm
    group_required = [u'manager']


class ManagerCategorieUpdateView(GroupRequiredMixin, UpdateView):
    model = Categorie
    form_class = CategoryForm
    success_url = reverse_lazy('manager-categorie-list')
    template_name = 'news_blog/manager_categorie_update.html'
    group_required = [u'manager']


class ManagerUserListView(GroupRequiredMixin, ListView):
    model = User
    template_name = 'users/manager_user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['id']
    group_required = [u'manager']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        # context for filter
        context['user_types'] = UserType.objects.all()

        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_superuser=False).exclude(user_type__name='manager')
        search = self.request.GET.get('search', '')
        blocked = self.request.GET.get('blocked', '')
        staff = self.request.GET.get('staff', '')
        active = self.request.GET.get('active', '')

        if blocked:
            blocked = blocked == 'True'
            queryset = queryset.filter(is_blocked=blocked)

        if staff:
            staff = staff == 'True'
            queryset = queryset.filter(is_staff=staff)

        if active:
            active = active == 'True'
            queryset = queryset.filter(is_active=active)

        if search.strip():
            queryset = queryset.filter(first_name__contains=search)

        return queryset


class ManagerUserUpdateView(GroupRequiredMixin, UpdateView):
    model = User
    form_class = ManagersUserUpdateForm
    success_url = reverse_lazy('manager-user-list')
    template_name = 'users/manager_user_update.html'
    group_required = [u'manager']


class ManagerRestorePostListView(GroupRequiredMixin, ListView):
    model = PostRecycle
    template_name = 'news_blog/managers_restore_post_table.html'
    context_object_name = 'deleted_items'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['id']
    group_required = [u'manager']

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
        queryset = super().get_queryset().filter(deleted_by=self.request.user)

        queryset = get_queryset_for_deleted_on(
            request=self.request,
            queryset=queryset
        )

        get_queryset_for_search(
            request=self.request,
            queryset=queryset
        )

        return queryset


class ManagerRestorePostConfirmView(GroupRequiredMixin, FormView):
    form_class = RestoreConfirmationForm
    template_name = 'news_blog/editor_restore_post_confirm.html'
    success_url = reverse_lazy('manager-restore-post-list')
    group_required = [u'manager']

    def get_form_kwargs(self):
        kwargs = super(ManagerRestorePostConfirmView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk')
        return kwargs

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        obj = PostRecycle.objects.get(id=pk)
        post = obj.post
        post.status = PostStatus.objects.get(name='inactive')

        PostStatusRecord(
            changed_by=self.request.user,
            post=post,
            status=post.status
        ).save()

        post.save()
        obj.delete()
        return HttpResponseRedirect(self.get_success_url())


class ManagerAddCommentView(GroupRequiredMixin, FormView):
    model = ManagerComment
    form_class = ManagersAddCommentForm
    success_url = reverse_lazy('manager-post-list')
    template_name = 'custom_admin/manager_add_comment.html'
    group_required = [u'manager']

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', '')
        if not (pk and Post.objects.filter(id=pk, post_type='MANUAL').exists()):
            self.template_name = '404.html'
        return self.render_to_response(self.get_context_data())

    def get_form_kwargs(self):
        kwargs = super(ManagerAddCommentView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk')
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        query = ManagerComment.objects.filter(manager=self.request.user, post_id=pk)
        if query.exists():
            obj = query.first()
            obj.comment = form.cleaned_data.get('comment')
            obj.save()
        else:
            ManagerComment(
                manager=self.request.user,
                post=Post.objects.get(id=pk),
                comment=form.cleaned_data.get('comment')
            ).save()
        return HttpResponseRedirect(self.get_success_url())
