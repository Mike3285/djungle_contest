from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404

from django.urls import path

urlpatterns = [
    path('contest=<str:code>', views.check_contest, name='ciaone'),
]
