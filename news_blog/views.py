from django.shortcuts import render, redirect, reverse
from .models import Post
from django.views import View
from django.http import HttpResponse


class HomeView(View):
    def get(self, request):
        posts = Post.objects.filter(status='ACT')
        return render(request, 'news_blog/home.html', context={"posts": posts})

