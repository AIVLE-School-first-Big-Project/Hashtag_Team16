from django.urls import path
from . import views




app_name = 'qna'

urlpatterns = [
    path('', views.qna_board, name='qna_board'),
    path('create/', views.create, name='qna_create'),
    path('post/<int:pk>/', views.post, name='qna_post'),
    path('post/<int:pk>/p_modify/', views.p_modify, name='p_modify'),
    path('post/<int:pk>/comment', views.comment, name='comment'),
]

