from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import USER
from django.utils import timezone
from django.http import HttpResponse
from .models import USER
# Create your views here.

app_name = 'mypage'

def mypage(request):
    return render(request, 'mypage/mypage.html')

def modify(request):
    return render(request, 'mypage/modify.html')