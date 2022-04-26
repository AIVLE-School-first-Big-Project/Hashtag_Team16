from django.shortcuts import render, redirect
from .models import USER, LOG
from django.utils import timezone
from django.http import HttpResponse
from django.core.paginator import Paginator

# Create your views here.

def mypage(request):
    try:
        user = USER.objects.get(user_id=request.session['user_id']).user_id
        log_list = LOG.objects.all()
        now_page = request.GET.get('page', 1)
        p = Paginator(log_list, 10)
        now_page = int(now_page)
        info = p.get_page(now_page)
        return render(request, 'mypage/mypage.html', {'user':user, 'log_list':log_list, 'info':info})
    
    except KeyError:
        return redirect('/')
    
    
def modify(request):
    try:
        user = USER.objects.get(user_id=request.session['user_id']).user_id
        return render(request, 'mypage/modify.html')
    except KeyError:
        return redirect('/')
