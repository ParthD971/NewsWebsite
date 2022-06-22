from django.shortcuts import render, redirect
from users.models import CustomUser as User, UserType
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group
from news_blog.models import ApplicationNotification, Post, PostStatus, Categorie
from django.db.models import Q
from news_blog.paginators import CustomPaginator
from .forms import CategoryForm

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
    template_name = 'users/application_notification_table.html'
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

    def get_queryset(self):
        return Post.objects.filter(Q(status__name='pending') | Q(status__name='rejected'), author=self.request.user)


class PostsCreateView(CreateView):
    model = Post
    template_name = 'news_blog/create_post_form.html'
    fields = ['title', 'content', 'category', 'image']
    success_url = reverse_lazy('editors_news_posts_table')

    def form_valid(self, form):
        post_obj = form.instance
        post_obj.author = self.request.user
        post_obj.status = PostStatus.objects.get(name='pending')
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
        return super(EditorsPostUpdateView, self).form_valid(form)


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
        page = self.request.GET.get('page', 1)
        posts = Post.objects.all()
        paginator = self.paginator_class(posts, self.paginate_by)

        posts = paginator.page(page)
        posts.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = posts
        return context


class ManagersPostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'category', 'image', 'status']
    success_url = reverse_lazy('managers_news_posts_table')
    template_name = 'news_blog/post_update_form.html'

    def form_valid(self, form):
        post_obj = form.instance
        # if image is updated then remove old image
        return super(ManagersPostUpdateView, self).form_valid(form)


class CategoryListView(ListView):
    model = Categorie
    template_name = 'news_blog/categories_table.html'
    context_object_name = 'categories'


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        users = User.objects.all()
        paginator = self.paginator_class(users, self.paginate_by)

        users = paginator.page(page)
        users.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = users
        return context

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class ManagersUserUpdateView(UpdateView):
    model = User
    fields = ['is_blocked']
    success_url = reverse_lazy('managers_users_table')
    template_name = 'users/managers_user_update_form.html'

