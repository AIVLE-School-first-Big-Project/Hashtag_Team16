from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index.as_view()),
    path('function/', views.function.as_view()),
    path('image/', views.image_upload_save.as_view()),
    path('hashtag/', views.hashtag.as_view()),
    path('gan_image/', views.GAN_image.as_view()),
    path('likes/', views.likes.as_view()),
    path('influence/', views.influence.as_view()),
]

