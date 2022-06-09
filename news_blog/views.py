from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    if request.user.is_authenticated:
        print(request.user)
    return render(request, 'news_blog/home.html')
