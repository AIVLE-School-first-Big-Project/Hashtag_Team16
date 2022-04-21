from venv import create
from django.urls import path
from . import views

app_name = 'qna'

urlpatterns = [
    path('', views.qna_board, name='qna_board'),
    path('create/', views.create, name='qna_create'),
    path('post/<int:pk>/', views.post, name='qna_post'),
]

