from django.shortcuts import render
from .models import Articles
# Create your views here.

def all_articles(request):
    articles = Articles.objects.all()[::-1]
    return render(request,'All-Articles.html',{'articles':articles})