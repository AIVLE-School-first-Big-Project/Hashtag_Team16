from django.urls import path
from .views import *
from member.views import *

urlpatterns = [
    path('login/', login_custom, name='login_custom'),
]
