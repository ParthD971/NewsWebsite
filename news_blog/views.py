from .models import Post, ApplicationNotification, NotificationStatus, NotificationType, Follow, PostNotification
from django.views.generic import ListView, DetailView, View
from .paginators import CustomPaginator
from django.views.generic.edit import FormView
from .forms import ManagerApplicationForm, EditorApplicationForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from users.models import CustomUser as User
import os
from django.http import HttpResponse


class HomeView(ListView):
    model = Post
    template_name = 'news_blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    paginator_class = CustomPaginator
    ordering = ['-created_on']

    def get_queryset(self):
        queryset = super().get_queryset().filter(status__name='active')

        # for serach filter
        search = self.request.GET.get('search', None)
        if search:
            return queryset.filter(Q(title__contains=search) | Q(content__contains=search))

        # for author filter
        author_display_name = self.request.GET.get('author', '')
        if author_display_name:
            # filter by display name
                queryset = queryset.filter(author_display_name=author_display_name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        posts = self.get_queryset()
        paginator = self.paginator_class(posts, self.paginate_by)

        posts = paginator.page(page)
        posts.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = posts


        if self.request.user.is_authenticated and self.request.user.user_type and self.request.user.user_type.name == 'consumer':
            context['notifications'] = PostNotification.objects.filter(user=self.request.user, seen=False).order_by('-id')

        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'news_blog/news_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if self.object.status.name != 'active':
            self.template_name = '404.html'

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            post_id = self.kwargs.get('pk', '')
            post = Post.objects.get(id=post_id)
            author = post.author
            if author:
                # manaul
                if Follow.objects.filter(user=user, author=author).exists():
                    context['following'] = True
                else:
                    context['following'] = False
            else:
                # scraped
                if Follow.objects.filter(user=user, author_name=post.author_display_name).exists():
                    context['following'] = True
                else:
                    context['following'] = False

        return context


# login required
class ManagerApplicationView(SuccessMessageMixin, FormView):
    template_name = 'news_blog/manager_application.html'
    form_class = ManagerApplicationForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(ManagerApplicationView, self).get_form_kwargs()
        print(kwargs)
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        if form.cleaned_data.get('check'):
            try:
                current_user = self.request.user
                notification_type = NotificationType.objects.get(name='manager request')
                status = NotificationStatus.objects.get(name='pending')
                application_notification = ApplicationNotification(user=current_user, notification_type=notification_type, status=status)
                application_notification.save()
                messages.success(self.request, 'Application for manager submitted.')
            except NotificationType.DoesNotExist as e:
                messages.error(self.request, 'NotificationType not exists: ' + e)
            except NotificationStatus.DoesNotExist as e:
                messages.error(self.request, 'NotificationStatus not exists: ' + e)
        else:
            messages.error(self.request, 'Form not valid')
        return super().form_valid(form)


# login required
class EditorApplicationView(SuccessMessageMixin, FormView):
    template_name = 'news_blog/editor_application.html'
    form_class = EditorApplicationForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(EditorApplicationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        if form.cleaned_data.get('check'):
            try:
                current_user = self.request.user
                notification_type = NotificationType.objects.get(name='editor request')
                status = NotificationStatus.objects.get(name='pending')
                application_notification = ApplicationNotification(user=current_user, notification_type=notification_type, status=status)
                application_notification.save()
                messages.success(self.request, 'Application for editor submitted.')
            except NotificationType.DoesNotExist as e:
                messages.error(self.request, 'NotificationType not exists: ' + e)
            except NotificationStatus.DoesNotExist as e:
                messages.error(self.request, 'NotificationStatus not exists: ' + e)
        else:
            messages.error(self.request, 'Form not valid')
        return super().form_valid(form)


from django.urls import resolve
class FollowView(View):
    def get(self, request, **kwargs):
        user = request.user
        author_id = request.GET.get('author_id', '')
        author_name = request.GET.get('author_name', '')
        if author_id:
            author = User.objects.filter(id=author_id, user_type__name='editor')
            if not author.exists():
                messages.error(request, 'Author not valid.')
            else:
                author = author.first()
                # manual post
                follow_obj = Follow.objects.filter(author__id=author_id, user__id=user.id)
                is_following = follow_obj.exists()
                if is_following:
                    # un follow it
                    follow_obj.first().delete()
                    messages.success(request, f'Un-followed {author.first_name}')
                    print('un-following')
                else:
                    Follow(author=author, user=user, author_name=author.first_name).save()
                    messages.success(request, f'Started following {author.first_name}')
                    print('following')
        elif author_name:
            # validating if this name exists
            if not Post.objects.filter(author_display_name=author_name).exists():
                messages.error(request, 'Author name not valid.')
            else:
                follow_obj = Follow.objects.filter(author_name=author_name, user__id=user.id)
                is_following = follow_obj.exists()
                if is_following:
                    # un follow it
                    follow_obj.first().delete()
                    messages.success(request, f'Un-followed {author_name}')
                    print('un-following')
                else:
                    Follow(user=user, author_name=author_name).save()
                    messages.success(request, f'Started following {author_name}')
                    print('following')

        return redirect('news_detail', pk=self.kwargs.get('pk', ''))


def notification_seen(request, **kwargs):
    noti_id = request.GET.get('pk', '')
    post_notifications = PostNotification.objects.filter(id=noti_id)
    if not post_notifications.exists():
        return HttpResponse('Does not exists')
    else:
        post_notification = post_notifications.first()
        post_notification.seen = True
        post_notification.save()

    return HttpResponse('Done')


class PostNotificationListView(ListView):
    model = PostNotification
    template_name = 'news_blog/post_notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20
    ordering = ['-id']
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

        context['unseen_notifications'] = PostNotification.objects.filter(user=self.request.user, seen=False)


        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user, seen=True)
        # search = self.request.GET.get('search', '')
        # editor_display_name = self.request.GET.get('editor', '').strip()


        # if editor_display_name:
        #     queryset = queryset.filter(author_display_name=editor_display_name)
        #
        # if search:
        #     queryset = queryset.filter(Q(title__contains=search) | Q(content__contains=search))
        return queryset





def run_scraper(request):
    os.system('python manage.py crawl "sports"')
    return HttpResponse('Done')


