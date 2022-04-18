from django.urls import path
from .views import *
from member.views import *

urlpatterns = [
    path('login/custom/', login_custom, name='login_custom'),
]
