from .models import Post, ApplicationNotification, NotificationStatus, NotificationType
from django.views.generic import ListView
from .paginators import CustomPaginator
from django.views.generic.edit import FormView
from .forms import ManagerApplicationForm, EditorApplicationForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class HomeView(ListView):
    model = Post
    template_name = 'news_blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    paginator_class = CustomPaginator
    ordering = ['-created_on']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        posts = Post.objects.all()
        paginator = self.paginator_class(posts, self.paginate_by)

        posts = paginator.page(page)
        posts.adjusted_elided_pages = paginator.get_elided_page_range(page)
        context['page_obj'] = posts
        return context


# login required
class ManagerApplicationView(SuccessMessageMixin, FormView):
    template_name = 'news_blog/manager_application.html'
    form_class = ManagerApplicationForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(ManagerApplicationView, self).get_form_kwargs()
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


