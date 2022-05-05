from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index),
    path('function/', views.function.as_view()),
    path('image/', views.image_upload_save.as_view()),
    path('hashtag/', views.hashtag.as_view()),
]

