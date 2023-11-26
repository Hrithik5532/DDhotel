from django.shortcuts import render
from .models import Articles
from taggit.models import Tag
from django.db.models import Q
from Product.models import Product
# Create your views here.

def all_articles(request):
    articles = Articles.objects.all()[::-1]
    if request.GET.get('tag') :
        articles = Articles.objects.filter(tags__name = request.GET.get('tag'))[::-1]

    if request.GET.get('search') :
        query = request.GET.get('search') 
        
        articles = Articles.objects.filter(
            Q(name__icontains=query) |
            Q(content__icontains=query)
        )[::-1]

    tags = Tag.objects.all()[::-1]
    return render(request,'All-Articles.html',{'tags':tags,'articles':articles})

def article_main(request,name):
    article = Articles.objects.get(name=name)
    articles = Articles.objects.all()
    tags =Tag.objects.all()
    top_selling_products = Product.objects.all()[::4]
    return render(request,'Article-singal.html',{'article':article,'articles':articles,'tags':tags,'top_selling_products':top_selling_products})