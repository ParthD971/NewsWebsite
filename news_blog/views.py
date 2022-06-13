from django.shortcuts import render
from .models import Post
from django.views import View


class HomeView(View):
    def get(self, request):
        posts = Post.objects.filter(status='ACT')
        return render(request, 'news_blog/home.html', context={"posts": posts})

