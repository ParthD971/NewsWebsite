from django.shortcuts import render
from django.http import HttpResponse
from .models import Post


def home(request):
    posts = Post.objects.filter(status='ACT')
    return render(request, 'news_blog/home.html', {'posts': posts})
