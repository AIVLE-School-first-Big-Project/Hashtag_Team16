from venv import create
from django.urls import path
from . import views
from .views import *
from qna.views import *


app_name = 'qna'

urlpatterns = [
    path('', views.qna_board, name='qna_board'),
    path('create/', views.create, name='qna_create'),
    path('post/<int:pk>/', views.post, name='qna_post'),
    path('', views.logout_custom, name='logout_custom'),
    #path('update/<int:pk>/', views.post, name='qna_update')
    #path('update/', views.update, name='qna_update')
]

