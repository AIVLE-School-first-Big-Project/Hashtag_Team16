from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from .models import USER
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import auth 
from django.contrib import messages
# 나중에 쓸거야!
# from django.contrib.auth.hashers import check_password
# from django.contrib.auth import update_session_auth_hash 
# from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.auth.decorators import login_required 
# from django.contrib.auth.hashers import make_password



# Create your views here.

# user 출력
def user(request):
   user_list = USER.objects.all()
   return render(
        request,
        'member/line.html',
        {'user_list': user_list }
   )


def login_custom(request):
    if request.method == 'POST':
        u_id = request.POST.get('user_id')
        u_pw = request.POST.get('user_pw')
        try:
            user = USER.objects.get(user_id = u_id, pw = u_pw)
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
        
        u = USER(
            user_id=u_id, pw=u_pw, name=u_name, 
            birth_year=b_year,birth_month=b_month,birth_day=b_day, phone_num=p_num, email=email, usage_count=0)
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
        return redirect('/')
    


    return redirect('/')

# 비밀번호 변경
def change_password(request):
    if request.method == "POST":
        o_pw = request.POST.get('origin_password')
        n_pw = request.POST.get('new_password')
        n_pw2 = request.POST.get('confirm_password')
        
        print(request.session['user_id'])
        
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
            return redirect('/')
        


def change_info(request):
    
    if request.method == 'POST':
        user_id = request.session['user_id']
        print(user_id)
        user_inst =  USER.objects.get(user_id=user_id)
        new_name = request.POST['name']
        new_email = request.POST['email']
        new_phone_num = request.POST['phone_num']
        
        user_inst.name = new_name
        user_inst.email = new_email
        user_inst.phone_num = new_phone_num
        user_inst.save()
        return redirect('../../member/line') #user 변경 확인을 위해 user list 출력창입니다~

    else: 
        try:
            user = USER.objects.get(user_id=request.session['user_id']).user_id
            return render(request, 'member/change_info.html')
        except KeyError:
            return redirect('/')
        