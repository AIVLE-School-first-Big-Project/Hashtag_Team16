from django.shortcuts import render
from django.http import HttpResponse

def index1(request):
    return HttpResponse('<u>Hello</u>')
# Create your views here.

def index(request):
    return render(request, 'main/index.html')