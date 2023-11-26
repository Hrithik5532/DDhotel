from django.urls import path

from .views import *
urlpatterns = [
    path('',all_articles,name="all_articles"),
    path('/(?P<name>[-a-zA-Z0-9_]+)\\Z',article_main,name="article_main")
]