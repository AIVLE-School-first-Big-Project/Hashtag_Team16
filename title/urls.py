from django.urls import path
from . import views

app_name = 'title'

urlpatterns = [
    path('', views.index),
    path('need_login', views.need_login),
]

