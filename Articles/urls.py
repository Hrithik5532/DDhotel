from django.urls import path

from .views import *
urlpatterns = [
    path('',all_articles,name="all_articles")
]