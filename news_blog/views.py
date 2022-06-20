from django.shortcuts import render, redirect, reverse
from .models import Post
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse


class HomeView(ListView):
    queryset = Post.objects.all()
    template_name = 'news_blog/home.html'
    context_object_name = 'posts'

    # def get_queryset(self):
    #     return self.queryset.filter(status='ACT')
