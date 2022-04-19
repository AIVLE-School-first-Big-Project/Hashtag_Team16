from django.urls import path
from .views import *
from member.views import *

urlpatterns = [
    path('line/', user, name='line'),
    path('login/', login_custom, name='login_custom'),
    path('signup/', signup_custom, name='signup_custom'),
    path('logout/', logout_custom, name='logout_custom'),
]
 


       