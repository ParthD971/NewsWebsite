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
    PostRecycle
)
from django.db.models import Q
from news_blog.paginators import CustomPaginator
from .forms import CategoryForm, ManagersPostUpdateForm, RestoreConfirmationForm, DeleteConfirmationForm
from datetime import datetime
from news_blog.constants import DEFAULT_IMAGE_NAME


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

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_superuser=False)
        search = self.request.GET.get('search', '')
        if search.strip():
            return queryset.filter(Q(first_name__contains=search))
        return queryset


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
        old_user_obj = User.objects.get(id=instance.id)
        if old_user_obj.user_type != instance.user_type:
            print('-----')
            instance.groups.clear()
            my_group = Group.objects.get(name=instance.user_type.name)
            my_group.user_set.add(instance)
        return super(UserUpdateView, self).form_valid(form)


class ApplicationNotificationListView(ListView):
    model = ApplicationNotification
    template_name = 'users/application_notification_table.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        queryset = super().get_queryset().filter(status__name='pending')
        search = self.request.GET.get('search', '')
        if search.strip():
            return queryset.filter(Q(user__first_name__contains=search))
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
    ordering = ['-created_on']
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
        context['statuses'] = PostStatus.objects.filter(Q(name='rejected') | Q(name='pending'))

        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            Q(status__name='pending') | Q(status__name='rejected'),
            author=self.request.user
        )
        search = self.request.GET.get('search', '')
        created_on = self.request.GET.get('created_on', '').strip()
        category = self.request.GET.get('category', '').strip()
        status = self.request.GET.get('status', '').strip()

        if created_on:
            created_on = datetime.strptime(created_on, '%Y-%m-%d').date()
            queryset = queryset.filter(created_on=created_on)

        if category:
            queryset = queryset.filter(category__name=category)

        if status:
            queryset = queryset.filter(status__name=status)

        if search:
            queryset = queryset.filter(Q(title__contains=search) | Q(content__contains=search))

        return queryset


class PostsCreateView(CreateView):
    model = Post
    template_name = 'news_blog/create_post_form.html'
    fields = ['title', 'content', 'category', 'image']
    success_url = reverse_lazy('editors_news_posts_table')

    def form_valid(self, form):
        post_obj = form.instance
        print(post_obj.image)
        post_obj.author = self.request.user
        post_obj.status = PostStatus.objects.get(name='pending')
        post_obj.author_display_name = self.request.user.first_name
        # post_obj.post_type = default set to Manual
        # if image is updated then remove old image
        return super(PostsCreateView, self).form_valid(form)


class EditorsPostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'category', 'image']
    success_url = reverse_lazy('editors_news_posts_table')
    template_name = 'news_blog/post_update_form.html'

    def form_valid(self, form):
        post_obj = form.instance
        post_obj.status = PostStatus.objects.get(name='pending')

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
    ordering = ['-created_on']
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
        # context['authors'] = self.get_queryset().order_by('author_display_name').values('author_display_name').distinct()
        context['authors'] = Post.objects.exclude(Q(status__name='rejected') | Q(status__name='deleted')).order_by('author_display_name').values(
            'author_display_name').distinct()

        return context

    def get_queryset(self):
        queryset = super().get_queryset().exclude(Q(status__name='rejected') | Q(status__name='deleted'))
        search = self.request.GET.get('search', '')
        created_on = self.request.GET.get('created_on', '').strip()
        category = self.request.GET.get('category', '').strip()
        status = self.request.GET.get('status', '').strip()
        editor_display_name = self.request.GET.get('editor', '').strip()

        if created_on:
            created_on = datetime.strptime(created_on, '%Y-%m-%d').date()
            queryset = queryset.filter(created_on=created_on)

        if category:
            queryset = queryset.filter(category__name=category)

        if status:
            queryset = queryset.filter(status__name=status)

        if editor_display_name:
            queryset = queryset.filter(author_display_name=editor_display_name)

        if search:
            queryset = queryset.filter(Q(title__contains=search) | Q(content__contains=search))
        return queryset


class ManagersPostUpdateView(UpdateView):
    model = Post
    # fields = ['title', 'content', 'category', 'image', 'status']
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
                if old_status == 'pending' or old_status == 'inreview':
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
        queryset = super().get_queryset().filter(is_staff=False)
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
    fields = ['is_blocked']
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
        post.save()
        obj.delete()
        return HttpResponseRedirect(self.get_success_url())

