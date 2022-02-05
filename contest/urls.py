from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404

from django.urls import re_path

urlpatterns = [
    path('', views.check_contest, name='check_winner'),
    path('new_user', views.create_user, name='create_user'),
    path('login', views.login_user, name='login_user'),
]
