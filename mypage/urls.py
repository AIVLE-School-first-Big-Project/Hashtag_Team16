from django.urls import path
from .views import *
from member.views import *

app_name = 'mypage'

urlpatterns = [
    path('', mypage, name='mypage'),
    path('changepw/', change_password, name='change_password'),
]