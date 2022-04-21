from django.urls import path
from .views import *
from member.views import *

from mypage import views

urlpatterns = [
    path('', views.mypage, name='mypage'),
    path('modify/', views.modify, name='modify'),
]