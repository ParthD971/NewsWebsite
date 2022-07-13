from django.shortcuts import render
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from news_blog.models import (
    Post,
    PostStatus,
    Categorie,
    PostRecycle,
    PostStatusRecord,
)
from django.db.models import Q
from news_blog.paginators import CustomPaginator
from custom_admin.forms import (
    RestoreConfirmationForm,
    DeleteConfirmationForm,
    EditorsPostUpdateForm
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


class EditorMainPageView(GroupRequiredMixin, View):
    group_required = [u'editor']

    def get(self, request):
        return render(
            request=request,
            template_name="custom_admin/editor_main_page.html",
            context={}
        )


class EditorPostListView(GroupRequiredMixin, ListView):
    model = Post
    template_name = 'news_blog/editor_post_list.html'
    context_object_name = 'posts'
    paginate_by = 20
    ordering = ['-created_on', '-id']
    paginator_class = CustomPaginator
    group_required = [u'editor']

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
        context['statuses'] = PostStatus.objects.all().exclude(Q(name='deleted'))

        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            ~Q(status__name='deleted'),
            author=self.request.user
        )
        search = self.request.GET.get('search', '')
        status = self.request.GET.get('status', '').strip()

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

        if search:
            queryset = queryset.filter(Q(title__contains=search) | Q(content__contains=search))

        return queryset


class EditorPostCreateView(GroupRequiredMixin, CreateView):
    model = Post
    template_name = 'news_blog/editor_post_create.html'
    fields = ['title', 'content', 'category', 'image', 'premium']
    success_url = reverse_lazy('editor-post-list')
    group_required = [u'editor']

    def form_valid(self, form):
        post_obj = form.instance
        print(post_obj.image)
        post_obj.author = self.request.user
        post_obj.status = PostStatus.objects.get(name='pending')
        post_obj.author_display_name = self.request.user.first_name
        # post_obj.post_type = default set to Manual
        redirect_link = super(EditorPostCreateView, self).form_valid(form)

        post = self.object
        PostStatusRecord(
            changed_by=self.request.user,
            post=post,
            status=post.status
        ).save()

        return redirect_link


class EditorPostUpdateView(GroupRequiredMixin, UpdateView):
    model = Post
    form_class = EditorsPostUpdateForm
    success_url = reverse_lazy('editor-post-list')
    template_name = 'news_blog/manager_editor_post_update.html'
    group_required = [u'editor']

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
            remove_and_update_image_for_post(old_post_obj=Post.objects.get(id=post_obj.id))

        return super(EditorPostUpdateView, self).form_valid(form)


class EditorPostDeleteView(GroupRequiredMixin, FormView):
    form_class = DeleteConfirmationForm
    template_name = 'news_blog/editor_post_delete.html'
    success_url = reverse_lazy('editor-post-list')
    group_required = [u'editor']

    def get_form_kwargs(self):
        kwargs = super(EditorPostDeleteView, self).get_form_kwargs()
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


class EditorRestorePostListView(GroupRequiredMixin, ListView):
    model = PostRecycle
    template_name = 'news_blog/editor_restore_post_list.html'
    context_object_name = 'deleted_items'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['id']
    group_required = [u'editor']

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


class EditorRestorePostConfirmView(GroupRequiredMixin, FormView):
    form_class = RestoreConfirmationForm
    template_name = 'news_blog/editor_restore_post_confirm.html'
    success_url = reverse_lazy('editor-restore-post-list')
    group_required = [u'editor']

    def get_form_kwargs(self):
        kwargs = super(EditorRestorePostConfirmView, self).get_form_kwargs()
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


class EditorCommentListView(GroupRequiredMixin, ListView):
    model = ManagerComment
    template_name = 'custom_admin/editor_comment_list.html'
    context_object_name = 'comments'
    paginate_by = 20
    paginator_class = CustomPaginator
    ordering = ['id']
    group_required = [u'editor']

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
        queryset = super().get_queryset().filter(post__author=self.request.user)

        pk = self.kwargs.get('pk', '')
        queryset = queryset.filter(post_id=pk)

        return queryset
