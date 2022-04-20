from venv import create
from django.urls import path
from . import views

app_name = 'qna'

urlpatterns = [
    path('', views.qna_board, name='qna_board'),
    path('create/<int:pk>', views.create, name='create'),
]

