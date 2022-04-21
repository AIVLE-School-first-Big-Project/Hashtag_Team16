from django.urls import path
from .views import *
from member.views import *
from mypage import views

app_name = 'mypage'

urlpatterns = [
    path('', views.mypage, name='mypage'),
    path('changepw/', change_password, name='change_password'),
]

