from django.views.decorators.csrf import csrf_exempt
from .models import (
    Post,
    ApplicationNotification,
    NotificationStatus,
    NotificationType,
    Follow,
    PostNotification,
    PostView,
    Categorie,
)
from custom_admin.models import AdminNotification
from django.views.generic import ListView, DetailView, View, RedirectView, TemplateView
from .paginators import CustomPaginator
from django.views.generic.edit import FormView
from .forms import ManagerApplicationForm, EditorApplicationForm, PremiumApplicationForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from users.models import CustomUser as User, StripeCustomer
import os
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from datetime import datetime
from .permissions import GroupRequiredMixin, CheckPremiumUserMixin
from news_blog.helpers import get_paginated_context, is_mark_seen_success
from django.conf import settings
import stripe
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class HomeView(ListView):
    model = Post
    template_name = 'news_blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    paginator_class = CustomPaginator
    ordering = ['-created_on', '-id']

    def get_queryset(self):
        queryset = super().get_queryset().filter(status__name='active')

        # for search filter
        search = self.request.GET.get('search', '').strip()
        if search:
            return queryset.filter(Q(title__contains=search) | Q(content__contains=search))

        # for author filter
        author_display_name = self.request.GET.get('author', '').strip()
        if author_display_name:
            # filter by display name
            queryset = queryset.filter(author_display_name=author_display_name)

        # for date filter
        created_on = self.request.GET.get('created_on', '').strip()
        if created_on:
            created_on = datetime.strptime(created_on, '%Y-%m-%d').date()
            queryset = queryset.filter(created_on=created_on)

        categories = Categorie.objects.all()
        lis = [cat.name for cat in categories if self.request.GET.get(cat.name, '').strip()]
        if lis:
            queryset = queryset.filter(category__name__in=lis)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        if self.request.user.is_authenticated and self.request.user.user_type and self.request.user.user_type.name == 'consumer':
            context['notifications'] = PostNotification.objects.filter(user=self.request.user, seen=False).order_by(
                '-id')

        context['trending_posts'] = Post.objects.filter(status__name='active').order_by('-views')[:3]
        context['categories'] = Categorie.objects.all()
        context['authors'] = Post.objects.order_by('author_display_name').values('author_display_name').distinct()
        context['admin_notification'] = True
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'news_blog/news_detail.html'

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if self.object.status.name != 'active':
            return HttpResponseNotFound('Page Not Active')

        if self.object.premium:
            if not (request.user.is_authenticated and request.user.is_premium_user):
                return redirect('apply-for-premium-user')

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            post_id = self.kwargs.get('pk', '')
            post = Post.objects.get(id=post_id)
            author = post.author
            if author:
                # manual
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


class ManagerApplicationView(GroupRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'news_blog/manager_application.html'
    form_class = ManagerApplicationForm
    success_url = reverse_lazy('home')
    group_required = [u'consumer']

    def get_form_kwargs(self):
        kwargs = super(ManagerApplicationView, self).get_form_kwargs()
        print(kwargs)
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        current_user = self.request.user
        notification_type = NotificationType.objects.get(name='manager request')
        status = NotificationStatus.objects.get(name='pending')
        application_notification = ApplicationNotification(
            user=current_user,
            notification_type=notification_type,
            status=status
        )
        application_notification.save()
        messages.success(self.request, 'Application for manager submitted.')

        return super().form_valid(form)


class EditorApplicationView(GroupRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'news_blog/editor_application.html'
    form_class = EditorApplicationForm
    success_url = reverse_lazy('home')
    group_required = [u'consumer']

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
                application_notification = ApplicationNotification(user=current_user,
                                                                   notification_type=notification_type, status=status)
                application_notification.save()
                messages.success(self.request, 'Application for editor submitted.')
            except NotificationType.DoesNotExist as e:
                messages.error(self.request, 'NotificationType not exists: ' + e)
            except NotificationStatus.DoesNotExist as e:
                messages.error(self.request, 'NotificationStatus not exists: ' + e)
        else:
            messages.error(self.request, 'Form not valid')
        return super().form_valid(form)


class FollowView(GroupRequiredMixin, View):
    group_required = [u'consumer']

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
                else:
                    Follow(author=author, user=user, author_name=author.first_name).save()
                    messages.success(request, f'Started following {author.first_name}')
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
                else:
                    Follow(user=user, author_name=author_name).save()
                    messages.success(request, f'Started following {author_name}')

        return redirect('post-detail', pk=self.kwargs.get('pk', ''))


class PostNotificationListView(GroupRequiredMixin, ListView):
    model = PostNotification
    template_name = 'news_blog/post_notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20
    ordering = ['-id']
    paginator_class = CustomPaginator
    group_required = [u'consumer']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = get_paginated_context(
            context=context,
            request=self.request,
            queryset=self.get_queryset(),
            paginator_class=self.paginator_class,
            paginate_by=self.paginate_by
        )

        context['unseen_notifications'] = PostNotification.objects.filter(user=self.request.user, seen=False)
        return context

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, seen=True)


class NotificationSeenView(GroupRequiredMixin, View):
    group_required = [u'consumer']

    def get(self, request, **kwargs):
        if is_mark_seen_success(request=request, notification_class=PostNotification):
            return JsonResponse({'msg': 'Done'})
        return JsonResponse({'msg': 'Does not exists'})


class AddViewsView(View):
    def get(self, request, **kwargs):
        post_id = request.GET.get('pk', '')
        posts = Post.objects.filter(id=post_id)

        if not request.user.is_authenticated:
            return JsonResponse({'msg': 'views not added because user not logged in.'})
        if not posts.exists():
            return JsonResponse({'msg': 'views not added because post not valid.'})

        post = posts.first()
        post_view = PostView.objects.filter(user=request.user, post=post)
        if post_view.exists():
            return JsonResponse({'msg': 'views not added because already user have seen this post.'})
        PostView(
            user=request.user,
            post=post
        ).save()
        post.views += 1
        post.save()
        return JsonResponse({'msg': 'views added'})


class PremiumApplyView(GroupRequiredMixin, CheckPremiumUserMixin, TemplateView):
    template_name = 'news_blog/premium_user_application.html'
    group_required = [u'consumer']


class StripeConfig(GroupRequiredMixin, View):
    group_required = [u'consumer']

    @method_decorator(csrf_exempt)
    def get(self, request):
        stripe_config_ = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config_, safe=False)


# @csrf_exempt
# def stripe_config(request):
#     if request.method == 'GET':
#         stripe_config_ = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
#         return JsonResponse(stripe_config_, safe=False)


class CreateCheckoutSession(GroupRequiredMixin, View):
    group_required = [u'consumer']

    @method_decorator(csrf_exempt)
    def get(self, request):
        domain_url = request.build_absolute_uri(reverse_lazy('home'))
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


# @csrf_exempt
# def create_checkout_session(request):
#     if request.method == 'GET':
#         domain_url = request.build_absolute_uri(reverse_lazy('home'))
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         try:
#             checkout_session = stripe.checkout.Session.create(
#                 client_reference_id=request.user.id if request.user.is_authenticated else None,
#                 success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
#                 cancel_url=domain_url + 'cancel/',
#                 payment_method_types=['card'],
#                 mode='subscription',
#                 line_items=[
#                     {
#                         'price': settings.STRIPE_PRICE_ID,
#                         'quantity': 1,
#                     }
#                 ]
#             )
#             return JsonResponse({'sessionId': checkout_session['id']})
#         except Exception as e:
#             return JsonResponse({'error': str(e)})





class StripeWebhook(GroupRequiredMixin, View):

    @method_decorator(csrf_exempt)
    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']

            # Fetch all the required data from session
            client_reference_id = session.get('client_reference_id')
            stripe_customer_id = session.get('customer')
            stripe_subscription_id = session.get('subscription')

            # Get the user and create a new StripeCustomer
            user = User.objects.get(id=client_reference_id)
            StripeCustomer.objects.create(
                user=user,
                stripeCustomerId=stripe_customer_id,
                stripeSubscriptionId=stripe_subscription_id,
            )
            print(user.username + ' just subscribed.')

        return HttpResponse(status=200)

# @csrf_exempt
# def stripe_webhook(request):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None
#
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)
#
#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#
#         # Fetch all the required data from session
#         client_reference_id = session.get('client_reference_id')
#         stripe_customer_id = session.get('customer')
#         stripe_subscription_id = session.get('subscription')
#
#         # Get the user and create a new StripeCustomer
#         user = User.objects.get(id=client_reference_id)
#         StripeCustomer.objects.create(
#             user=user,
#             stripeCustomerId=stripe_customer_id,
#             stripeSubscriptionId=stripe_subscription_id,
#         )
#         print(user.username + ' just subscribed.')
#
#     return HttpResponse(status=200)

class SuccessPaymentView(GroupRequiredMixin, View):
    group_required = [u'consumer']

    def get(self, request):
        messages.success(request, 'Payment successful and you are now premium user!!!!')
        user = request.user
        user.is_premium_user = True
        user.save()
        return redirect('home')

# @login_required
# def success(request):
#     messages.success(request, 'Payment successful and you are now premium user!!!!')
#     user = request.user
#     user.is_premium_user = True
#     user.save()
#     return redirect('home')



class FailedPaymentView(GroupRequiredMixin, View):
    group_required = [u'consumer']

    def get(self, request):
        messages.error(request, 'Payment Failed!')
        return redirect('home')

# @login_required
# def cancel(request):
#     messages.success(request, 'Payment Failed')
#     return redirect('home')


class NotificationFromAdminView(GroupRequiredMixin, View):
    group_required = [u'consumer', u'manager', u'editor']

    def get(self, request):
        context = {}

        if request.user.is_authenticated:
            context['notifications'] = AdminNotification.objects.filter(receiver=request.user).order_by('-id')

        return render(
            request,
            template_name='news_blog/notification_from_admin.html',
            context=context
        )


class NotificationFromAdminSeenView(GroupRequiredMixin, View):
    group_required = [u'consumer', u'manager', u'editor']

    def get(self, request, **kwargs):
        if is_mark_seen_success(request=request, notification_class=AdminNotification):
            return JsonResponse({'msg': 'Done'})
        return JsonResponse({'msg': 'Does not exists'})


class RunScrapper(GroupRequiredMixin, View):
    group_required = [u'manager']

    def get(self, request):
        os.system('python manage.py crawl "sports"')
        return JsonResponse({'msg': 'Done'})
