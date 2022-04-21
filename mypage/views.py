from django.http import HttpResponse
from django.shortcuts import render, redirect
from sympy import re
from .models import USER
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import auth 
from .models import USER
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash # 비밀번호 변경 후 로그아웃 방지 --> 나중에 로그아웃하려면 삭제하면됨
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.hashers import make_password
# Create your views here.

# password 변경
#@login_required --> 향후 로그인했을 때만 기능 구현가능

def change_password(request):

    if request.method == "POST":
        e =  USER.objects.get(user_id='sh', pw='1234')
        request.session['user_id']= e.user_id
        request.session['pw']= e.pw
        user = USER.objects.get(user_id=request.session['user_id'], pw=request.session['pw'])
        origin_password = request.POST["origin_password"]
        
        if origin_password==user.pw:
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
            if new_password == confirm_password:

                # user.set_password(new_password)
                # user.save()
                user.pw = new_password
                user.save()
                #auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('../../member/line')
            else:
                return render(request, 'mypage/change_pw.html')
        else:
            return HttpResponse('<u>실!패!</u>')
    else:
        return render(request, 'mypage/change_pw.html')
app_name = 'mypage'

def mypage(request):
    return render(request, 'mypage/mypage.html')

def modify(request):
    return render(request, 'mypage/modify.html')
