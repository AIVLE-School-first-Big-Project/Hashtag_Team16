from django.urls import path
from .views import *
from member.views import *

app_name = 'member'

urlpatterns = [
    path('', mypage, name='mypage'),
    path('modify/', modify, name='modify'),
    
    path('line/', user, name='line'),
    path('login/', login_custom, name='login_custom'),
    path('signup/', signup_custom, name='signup_custom'),
    path('logout/', logout_custom, name='logout_custom'),
    path('changepw/', change_password, name='change_password'),
    path('changeinfo/', change_info, name='change_info'),
    path('information/', information, name='information'),
]