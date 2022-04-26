from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'title/index.html')

def need_login(request):
    return render(request, 'title/need_login.html')