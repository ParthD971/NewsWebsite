from django.shortcuts import render, redirect
from users.models import CustomUser as User, UserType
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
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
from .forms import (
    CategoryForm,
    ManagersPostUpdateForm,
    RestoreConfirmationForm,
    DeleteConfirmationForm,
    ManagersUserUpdateForm,
    ManagersAddCommentForm,
    EditorsPostUpdateForm
)
from datetime import datetime
from news_blog.constants import DEFAULT_IMAGE_NAME
from .models import ManagerComment, AdminNotification


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
    template_name = 'users/users_table.html'
    context_object_name = 'users'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        posts = self.get_queryset()
        paginator = self.paginator_class(posts, self.paginate_by)

        posts = paginator.page(page)
        posts.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = posts

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


class UserUpdateView(UpdateView):
    model = User
    fields = ['is_blocked']
    success_url = reverse_lazy('users_table')
    template_name = 'users/user_update_form.html'


class ApplicationNotificationListView(ListView):
    model = ApplicationNotification
    template_name = 'users/application_notification_table.html'
    context_object_name = 'notifications'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        posts = self.get_queryset()
        paginator = self.paginator_class(posts, self.paginate_by)

        posts = paginator.page(page)
        posts.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = posts

        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(status__name='pending')

        search = self.request.GET.get('search', '')
        if search.strip():
            return queryset.filter(Q(user__first_name__contains=search) | Q(user__last_name__contains=search))

        request_for = self.request.GET.get('request_for', '')
        if request_for:
            noti_type = 'manager request' if request_for == 'manager' else 'editor request'
            queryset = queryset.filter(notification_type__name=noti_type)

        return queryset


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


class EditorPanel(View):
    def get(self, request):
        return render(
            request=request,
            template_name="custom_admin/editor_panel.html",
            context={}
        )


class EditorsPostsListView(ListView):
    model = Post
    template_name = 'news_blog/editors_posts_table.html'
    context_object_name = 'posts'
    paginate_by = 20
    ordering = ['-created_on', '-id']
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        posts = self.get_queryset()
        paginator = self.paginator_class(posts, self.paginate_by)

        posts = paginator.page(page)
        posts.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = posts

        # context for filters
        context['categories'] = Categorie.objects.all()
        context['statuses'] = PostStatus.objects.all().exclude(Q(name='deleted'))

        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            ~Q(status__name='deleted'),
            author=self.request.user
        )
        search = self.request.GET.get('search', '')
        created_on = self.request.GET.get('created_on', '').strip()
        status = self.request.GET.get('status', '').strip()

        if created_on:
            created_on = datetime.strptime(created_on, '%Y-%m-%d').date()
            queryset = queryset.filter(created_on=created_on)

        caterories = Categorie.objects.all()
        lis = [cat.name for cat in caterories if self.request.GET.get(cat.name, '').strip()]
        if lis:
            queryset = queryset.filter(category__name__in=lis)

        if status:
            queryset = queryset.filter(status__name=status)

        if search:
            queryset = queryset.filter(Q(title__contains=search) | Q(content__contains=search))

        return queryset


class PostsCreateView(CreateView):
    model = Post
    template_name = 'news_blog/create_post_form.html'
    fields = ['title', 'content', 'category', 'image', 'premium']
    success_url = reverse_lazy('editors_news_posts_table')

    def form_valid(self, form):
        post_obj = form.instance
        print(post_obj.image)
        post_obj.author = self.request.user
        post_obj.status = PostStatus.objects.get(name='pending')
        post_obj.author_display_name = self.request.user.first_name
        # post_obj.post_type = default set to Manual
        redirect_link = super(PostsCreateView, self).form_valid(form)

        post = self.object
        PostStatusRecord(
            changed_by=self.request.user,
            post=post,
            status=post.status
        ).save()

        return redirect_link


class EditorsPostUpdateView(UpdateView):
    model = Post
    form_class = EditorsPostUpdateForm
    success_url = reverse_lazy('editors_news_posts_table')
    template_name = 'news_blog/post_update_form.html'

    def form_valid(self, form):
        post_obj = form.instance
        pending_status = PostStatus.objects.get(name='pending')
        if post_obj.status.name == 'rejected':
            PostStatusRecord(
                changed_by=self.request.user,
                post=post_obj,
                status=pending_status
            ).save()

        post_obj.status = pending_status

        # if image is updated then remove old image
        if 'image' in form.changed_data:
            old_post_obj = Post.objects.get(id=post_obj.id)
            if old_post_obj.image and old_post_obj.image.url.split('/')[-1] != DEFAULT_IMAGE_NAME:
                old_post_obj.image.delete(False)

        return super(EditorsPostUpdateView, self).form_valid(form)


class EditorsPostDeleteView(FormView):
    form_class = DeleteConfirmationForm
    template_name = 'news_blog/post_delete_form.html'
    success_url = reverse_lazy('editors_news_posts_table')

    def get_form_kwargs(self):
        kwargs = super(EditorsPostDeleteView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk')
        return kwargs

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        post_obj = Post.objects.get(id=pk)
        post_recycle_obj = PostRecycle(
            post=post_obj,
            deleted_by=self.request.user
        )
        post_obj.status = PostStatus.objects.get(name='deleted')

        PostStatusRecord(
            changed_by=self.request.user,
            post=post_obj,
            status=post_obj.status
        ).save()

        post_recycle_obj.save()
        post_obj.save()
        return HttpResponseRedirect(self.get_success_url())


class ManagerPanel(View):
    def get(self, request):
        return render(
            request=request,
            template_name="custom_admin/manager_panel.html",
            context={}
        )


class ManagersPostsListView(ListView):
    model = Post
    template_name = 'news_blog/managers_posts_table.html'
    context_object_name = 'posts'
    paginate_by = 20
    ordering = ['-created_on', '-id']
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        posts = self.get_queryset()
        paginator = self.paginator_class(posts, self.paginate_by)

        posts = paginator.page(page)
        posts.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = posts

        # context for filters
        context['categories'] = Categorie.objects.all()
        context['statuses'] = PostStatus.objects.all().exclude(Q(name='rejected') | Q(name='deleted'))
        context['authors'] = Post.objects.order_by('author_display_name').values(
            'author_display_name').distinct()

        return context

    def get_queryset(self):
        queryset = super().get_queryset().exclude(Q(status__name='rejected') | Q(status__name='deleted'))
        search = self.request.GET.get('search', '')
        created_on = self.request.GET.get('created_on', '').strip()

        status = self.request.GET.get('status', '').strip()
        editor_display_name = self.request.GET.get('editor', '').strip()

        if created_on:
            created_on = datetime.strptime(created_on, '%Y-%m-%d').date()
            queryset = queryset.filter(created_on=created_on)

        caterories = Categorie.objects.all()
        lis = [cat.name for cat in caterories if self.request.GET.get(cat.name, '').strip()]
        if lis:
            queryset = queryset.filter(category__name__in=lis)

        if status:
            queryset = queryset.filter(status__name=status)

        if editor_display_name:
            queryset = queryset.filter(author_display_name=editor_display_name)

        if search:
            queryset = queryset.filter(Q(title__contains=search) | Q(content__contains=search))
        return queryset


class ManagersPostUpdateView(UpdateView):
    model = Post
    form_class = ManagersPostUpdateForm
    success_url = reverse_lazy('managers_news_posts_table')
    template_name = 'news_blog/post_update_form.html'

    def get_form_kwargs(self):
        kwargs = super(ManagersPostUpdateView, self).get_form_kwargs()
        kwargs['object'] = self.get_object()
        return kwargs

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
                    print(followers)
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
            elif new_status == 'pending':
                pass

            # if status changed then update record
            PostStatusRecord(
                changed_by=self.request.user,
                post=post_obj,
                status=post_obj.status
            ).save()

        # if image is updated then remove old image
        if 'image' in form.changed_data:
            old_post_obj = Post.objects.get(id=post_obj.id)
            if old_post_obj.image and old_post_obj.image.url.split('/')[-1] != DEFAULT_IMAGE_NAME:
                old_post_obj.image.delete(False)
        return super(ManagersPostUpdateView, self).form_valid(form)


class CategoryListView(ListView):
    model = Categorie
    template_name = 'news_blog/categories_table.html'
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search.strip():
            return queryset.filter(Q(name__contains=search))
        return queryset


class CategoryCreateView(CreateView):
    model = Categorie
    template_name = 'news_blog/create_category_form.html'
    success_url = reverse_lazy('categories_table')
    form_class = CategoryForm


class CategoryUpdateView(UpdateView):
    model = Categorie
    form_class = CategoryForm
    success_url = reverse_lazy('categories_table')
    template_name = 'news_blog/category_update_form.html'

    def get_form_kwargs(self):
        kwargs = super(CategoryUpdateView, self).get_form_kwargs()
        kwargs['object'] = self.get_object()
        return kwargs


class ManagersUsersListView(ListView):
    model = User
    template_name = 'users/managers_users_table.html'
    context_object_name = 'users'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        users = self.get_queryset()
        paginator = self.paginator_class(users, self.paginate_by)

        users = paginator.page(page)
        users.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = users

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


class ManagersUserUpdateView(UpdateView):
    model = User
    form_class = ManagersUserUpdateForm
    success_url = reverse_lazy('managers_users_table')
    template_name = 'users/managers_user_update_form.html'


class ManagersRestorePostListView(ListView):
    model = PostRecycle
    template_name = 'news_blog/managers_restore_post_table.html'
    context_object_name = 'deleted_items'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        users = self.get_queryset()
        paginator = self.paginator_class(users, self.paginate_by)

        users = paginator.page(page)
        users.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = users

        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(deleted_by=self.request.user)
        search = self.request.GET.get('search', '')
        deleted_on = self.request.GET.get('deleted_on', '')

        if deleted_on:
            deleted_on = datetime.strptime(deleted_on, '%Y-%m-%d').date()
            queryset = queryset.filter(recycle_created_on=deleted_on)

        if search.strip():
            queryset = queryset.filter(Q(post__title__contains=search) | Q(post__content__contains=search))

        return queryset


class RestoreManagersNewsConfirmView(FormView):
    form_class = RestoreConfirmationForm
    template_name = 'news_blog/restore_news_confirmation.html'
    success_url = reverse_lazy('managers_restore_post_table')

    def get_form_kwargs(self):
        kwargs = super(RestoreManagersNewsConfirmView, self).get_form_kwargs()
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


class EditorsRestorePostListView(ListView):
    model = PostRecycle
    template_name = 'news_blog/editors_restore_post_table.html'
    context_object_name = 'deleted_items'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        users = self.get_queryset()
        paginator = self.paginator_class(users, self.paginate_by)

        users = paginator.page(page)
        users.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = users

        # context for filter
        # context['user_types'] = UserType.objects.all()

        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(deleted_by=self.request.user)
        search = self.request.GET.get('search', '')
        deleted_on = self.request.GET.get('deleted_on', '')

        if deleted_on:
            deleted_on = datetime.strptime(deleted_on, '%Y-%m-%d').date()
            queryset = queryset.filter(recycle_created_on=deleted_on)

        if search.strip():
            queryset = queryset.filter(Q(post__title__contains=search) | Q(post__content__contains=search))

        return queryset


class RestoreEditorsNewsConfirmView(FormView):
    form_class = RestoreConfirmationForm
    template_name = 'news_blog/restore_news_confirmation.html'
    success_url = reverse_lazy('editors_restore_post_table')

    def get_form_kwargs(self):
        kwargs = super(RestoreEditorsNewsConfirmView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk')
        return kwargs

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        obj = PostRecycle.objects.get(id=pk)
        post = obj.post
        post.status = PostStatus.objects.get(name='pending')
        PostStatusRecord(
            changed_by=self.request.user,
            post=post,
            status=post.status
        ).save()

        post.save()
        obj.delete()
        return HttpResponseRedirect(self.get_success_url())


class ManagersAddCommentView(FormView):
    model = ManagerComment
    # fields = ['comment']
    form_class = ManagersAddCommentForm
    success_url = reverse_lazy('managers_news_posts_table')
    template_name = 'custom_admin/add_comment.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', '')
        if not (pk and Post.objects.filter(id=pk, post_type='MANUAL').exists()):
            self.template_name = '404.html'
        return self.render_to_response(self.get_context_data())

    def get_form_kwargs(self):
        kwargs = super(ManagersAddCommentView, self).get_form_kwargs()
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


class EditorsCommentListView(ListView):
    model = ManagerComment
    template_name = 'custom_admin/editors_comment_list_table.html'
    context_object_name = 'comments'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        users = self.get_queryset()
        paginator = self.paginator_class(users, self.paginate_by)

        users = paginator.page(page)
        users.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = users

        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(post__author=self.request.user)

        pk = self.kwargs.get('pk', '')
        queryset = queryset.filter(post_id=pk)

        return queryset


class AdminCategoriesListView(ListView):
    model = Categorie
    template_name = 'news_blog/admin_categories_listview.html'
    context_object_name = 'categories'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        objects = self.get_queryset()
        paginator = self.paginator_class(objects, self.paginate_by)

        objects = paginator.page(page)
        objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = objects

        return context


class AdminFollowsListView(ListView):
    model = Follow
    template_name = 'news_blog/admin_follows_listview.html'
    context_object_name = 'follows'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        objects = self.get_queryset()
        paginator = self.paginator_class(objects, self.paginate_by)

        objects = paginator.page(page)
        objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = objects

        return context


class AdminNotificationStatusListView(ListView):
    model = NotificationStatus
    template_name = 'news_blog/admin_notification_status_listview.html'
    context_object_name = 'notification_statuses'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        objects = self.get_queryset()
        paginator = self.paginator_class(objects, self.paginate_by)

        objects = paginator.page(page)
        objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = objects

        return context


class AdminNotificationTypeListView(ListView):
    model = NotificationType
    template_name = 'news_blog/admin_notification_type_listview.html'
    context_object_name = 'notification_types'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        objects = self.get_queryset()
        paginator = self.paginator_class(objects, self.paginate_by)

        objects = paginator.page(page)
        objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = objects

        return context


class AdminPCMiddleListView(ListView):
    model = PCMiddle
    template_name = 'news_blog/admin_pcmiddle_listview.html'
    context_object_name = 'pcmiddles'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        objects = self.get_queryset()
        paginator = self.paginator_class(objects, self.paginate_by)

        objects = paginator.page(page)
        objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = objects

        return context


class AdminPostNotificationListView(ListView):
    model = PostNotification
    template_name = 'news_blog/admin_post_notification_listview.html'
    context_object_name = 'post_notifications'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        objects = self.get_queryset()
        paginator = self.paginator_class(objects, self.paginate_by)

        objects = paginator.page(page)
        objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = objects

        return context


class AdminPostRecycleListView(ListView):
    model = PostRecycle
    template_name = 'news_blog/admin_post_recycle_listview.html'
    context_object_name = 'post_recycles'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        objects = self.get_queryset()
        paginator = self.paginator_class(objects, self.paginate_by)

        objects = paginator.page(page)
        objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = objects

        return context


class AdminPostStatusRecordListView(ListView):
    model = PostStatusRecord
    template_name = 'news_blog/admin_post_status_record_listview.html'
    context_object_name = 'post_status_records'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        objects = self.get_queryset()
        paginator = self.paginator_class(objects, self.paginate_by)

        objects = paginator.page(page)
        objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = objects

        return context


class AdminPostStatusListView(ListView):
    model = PostStatus
    template_name = 'news_blog/admin_post_status_listview.html'
    context_object_name = 'post_statuses'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        objects = self.get_queryset()
        paginator = self.paginator_class(objects, self.paginate_by)

        objects = paginator.page(page)
        objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = objects

        return context


class AdminPostViewsListView(ListView):
    model = PostView
    template_name = 'news_blog/admin_post_view_listview.html'
    context_object_name = 'post_views'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        objects = self.get_queryset()
        paginator = self.paginator_class(objects, self.paginate_by)

        objects = paginator.page(page)
        objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = objects

        return context


class AdminPostsListView(ListView):
    model = Post
    template_name = 'news_blog/admin_posts_listview.html'
    context_object_name = 'posts'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        objects = self.get_queryset()
        paginator = self.paginator_class(objects, self.paginate_by)

        objects = paginator.page(page)
        objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = objects

        return context


class AdminUserTypeListView(ListView):
    model = UserType
    template_name = 'users/admin_user_type_listview.html'
    context_object_name = 'user_types'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        objects = self.get_queryset()
        paginator = self.paginator_class(objects, self.paginate_by)

        objects = paginator.page(page)
        objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = objects

        return context


class AdminManagerCommentsListView(ListView):
    model = ManagerComment
    template_name = 'custom_admin/admin_manager_comments_listview.html'
    context_object_name = 'manager_comments'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        objects = self.get_queryset()
        paginator = self.paginator_class(objects, self.paginate_by)

        objects = paginator.page(page)
        objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = objects

        return context


class AdminNotificationListView(ListView):
    model = AdminNotification
    template_name = 'custom_admin/admin_notification_listview.html'
    context_object_name = 'notifications'
    paginate_by = 20
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context for pagination
        page = self.request.GET.get('page', 1)
        objects = self.get_queryset()
        paginator = self.paginator_class(objects, self.paginate_by)

        objects = paginator.page(page)
        objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = objects

        return context


class AdminSendNotificationView(View):
    def get(self, request):
        context = {
            'users': User.objects.all().exclude(id=request.user.id)
        }
        return render(
            request,
            template_name='custom_admin/send_notification.html',
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
                template_name='custom_admin/send_notification.html',
                context=context
            )

        notis = [AdminNotification(receiver_id=user_id,message=message) for user_id in send_to_user_ids]
        AdminNotification.objects.bulk_create(notis)

        messages.success(request, 'Message sent successfully.')
        return redirect('admin_panel')

