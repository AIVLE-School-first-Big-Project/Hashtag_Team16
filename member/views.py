from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from sympy import re
from .models import *
from django.utils import timezone
from django.core.paginator import Paginator
import hashlib
from django.contrib.auth import logout as auth_logout

# Create your views here.
# mypage
def mypage(request):
    user = USER.objects.get(user_id=request.session['user_id']).user_id
    print(user)
    log_list = LOG.objects.filter(user=user)
    # 평점 스코어, 피드백 내용 기능 구현
    if 'score' in request.POST:
        print('post')
        real_log = log_list.get(log_id=request.POST.get('key'))
        real_log.service_score = request.POST.get('score')
        real_log.feedback = request.POST.get('feedback')
        print(real_log.service_score)
        print(real_log.feedback)

        if (real_log.service_score == '') or (real_log.feedback == ''):
            data = {'status':'F'}
            return JsonResponse(data)
        else:
            real_log.save()
            data = {'status':'T'}
            return JsonResponse(data)
    elif 'method' in request.POST:
        if request.POST.get('method') == 'Delete':
            user = USER.objects.get(user_id = request.POST.get('id'))
            user.delete()
            auth_logout(request)
            data = {'status':'delete_T'}
            return JsonResponse(data)
        else:
            data = {'status':'delete_F'}
            return JsonResponse(data)
    
    p = Paginator(log_list, 10)
    now_page = request.GET.get('page', 1)
    now_page = int(now_page)
    info = p.get_page(now_page)
    start_page = (now_page - 1) // 10 * 10 + 1
    end_page = start_page + 9
    if end_page > p.num_pages:
        end_page = p.num_pages
    # check box 선택 후 삭제
    if request.method == 'POST':
        print("delete check")
        delete_log = request.POST.getlist('id[]')   
        print(delete_log) 
        for id in delete_log:
            delete = LOG.objects.get(log_id=id)
            delete.delete()
    return render(request, 'member/mypage.html', {'user':user, 'log_list':log_list, 'info':info, 'page_range' : range(start_page, end_page + 1)})

def modify(request):
    return render(request, 'member/modify.html')

# user 출력
def user(request):
   user_list = USER.objects.all()
   return render(
        request,
        'member/line.html',
        {'user_list': user_list }
   )

salt='gdu'
#로그인
def login_custom(request):
    if request.method == 'POST':
        u_id = request.POST.get('user_id')
        u_pw = request.POST.get('user_pw')

        u_pw=hashlib.sha256(str(u_pw+salt).encode()).hexdigest()

        try:
            user = USER.objects.get(user_id = u_id, pw = u_pw)
            user.join_date = timezone.now()
            user.save()
        except USER.DoesNotExist as e:
            status = {'status' : 'F'}
            return JsonResponse(status)
        else:
            status = {'status' : 'T'}
            request.session['user_id'] = user.user_id
            request.session['user_name'] = user.name
        # 회원정보 조회 실패시 예외 발생
            return JsonResponse(status)

    else:
        # return JsonResponse(data, safe=False)
        return render(request, 'member/login_custom.html')

#회원가입
def signup_custom(request):
    if request.method == 'POST':
        u_id = request.POST.get('user_id')
        u_pw = request.POST.get('pw')
        u_pw2 = request.POST.get('pw2')
        u_name = request.POST.get('name')
        b_date = request.POST.get('birth_date')
        p_num = request.POST.get('phone_num')
        email = request.POST.get('email')
        
        b_year, b_month, b_day = b_date[:4], b_date[5:7], b_date[8:]
        
                
        if (u_id=='') or (u_pw=='') or (u_name=='') or (b_date=='') or (p_num=='') or (email==''):
            data = {'status': 'empty_error'}
            return JsonResponse(data)

        if USER.objects.filter(user_id = u_id).exists():
            data = {'status': 'id_error'}
            return JsonResponse(data)    
        
        if (u_pw != u_pw2):
            data = {'status':'pw_error'}
            return JsonResponse(data)
        
        if ('@' not in email):
            data = {'status':'email_error'}
            return JsonResponse(data)
            
        u_pw=hashlib.sha256(str(u_pw+salt).encode()).hexdigest()

        u = USER(
            user_id=u_id, pw=u_pw, name=u_name, 
            birth_year=b_year,birth_month=b_month,birth_day=b_day, phone_num=p_num, email=email, usage_count=0, join_date=timezone.now())
        u.date_joined = timezone.now()
        u.save()

        data = {'status':'T'}
        return JsonResponse(data)

    else:
        return render(request, 'member/signup_custom.html')

def logout_custom(request):
    try:
        user = USER.objects.get(user_id=request.session['user_id']).user_id
        
        del request.session['user_id']
        del request.session['user_name']

        request.session.flush()
        return redirect('/')
    
    except KeyError:
        return redirect('/need_login')

# 비밀번호 변경
def change_password(request):
    if request.method == "POST":
        o_pw = request.POST.get('origin_password')
        n_pw = request.POST.get('new_password')
        n_pw2 = request.POST.get('confirm_password')
        
        print(request.session['user_id'])
        
        o_pw=hashlib.sha256(str(o_pw+salt).encode()).hexdigest()

        user_inst =  USER.objects.get(user_id=request.session['user_id'])
        if (o_pw == '') or (n_pw == '') or (n_pw2 == ''):
            data = {'status':'empty_error'}
            return JsonResponse(data)
        
        if (n_pw != n_pw2):
            data = {'status':'cofirm_error'}
            return JsonResponse(data)
        
        if (user_inst.pw != o_pw):
            data = {'status':'pw_error'}
            return JsonResponse(data)

        n_pw=hashlib.sha256(str(n_pw+salt).encode()).hexdigest()

        if o_pw==user_inst.pw:
            user_inst.pw = n_pw
            user_inst.save()
            #auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            data = {'status':'T'}
            return JsonResponse(data)

    else:
        try:
            user = USER.objects.get(user_id=request.session['user_id']).user_id
            return render(request, 'member/change_pw.html')
        except KeyError:
            return redirect('/need_login')
        

def change_info(request):
    
    if request.method == 'POST':
        user_id = request.session['user_id']
        user_inst =  USER.objects.get(user_id=user_id)
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_num = request.POST.get('phone_num')
        
        if (name == '') or (email == '') or (phone_num == ''):
            data = {'status':'empty_error'}
            return JsonResponse(data)
        
        if ('@' not in email):
            data = {'status':'email_error'}
            return JsonResponse(data)

        user_inst.name = name
        user_inst.email = email
        user_inst.phone_num = phone_num

        user_inst.save()
        
        data = {'status':'T'}
        return JsonResponse(data)

            
    else: 
        try:
            user_id = request.session['user_id']
            user_inst =  USER.objects.get(user_id=user_id)
            name = user_inst.name
            email = user_inst.email
            phone_num = user_inst.phone_num
            return render(request, 'member/change_info.html',  {'name':name, 'email':email, 'phone_num':phone_num})
        except KeyError:
            return redirect('/need_login')     



def information(request):
   #user_list = USER.objects.all()
   print("개인정보 수정 page")
   return render(
        request,
        'member/information.html')
