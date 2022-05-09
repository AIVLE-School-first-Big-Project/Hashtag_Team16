from django.shortcuts import render, redirect
import json
from django.http import JsonResponse, HttpResponse
from .models import *
from django.utils import timezone
from django.core.paginator import Paginator
import hashlib
from django.contrib.auth import logout as auth_logout
import re
from .forms import RecoveryPwForm
from .forms import CustomSetPasswordForm 
from member.decorators import *
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import View
from .forms import RecoveryIdForm
import string
import random

# Create your views here.
# mypage
def mypage(request):
    user = USER.objects.get(user_id=request.session['user_id']).user_id  
    log_list = LOG.objects.filter(user=user)
    # 평점 스코어, 피드백 내용 기능 구현
    if 'score' in request.POST:
        real_log = log_list.get(log_id=request.POST.get('key'))
        real_log.service_score = request.POST.get('score')
        real_log.feedback = request.POST.get('feedback')
        
        if (real_log.service_score == '') or (real_log.feedback == ''):
            data = {'status':'F'}
            return JsonResponse(data)
        else:
            score = log_list.get(log_id=request.POST.get('key')).service_score
            fb = log_list.get(log_id=request.POST.get('key')).feedback
            if (score is not None) and (fb is not None):
                data = {'status':'exist_feedback'}
                return JsonResponse(data)
            else:
                real_log.save()
                data = {'status':'T'}
                return JsonResponse(data)
    # elif 'method' in request.POST:
    #     if request.POST.get('method') == 'Delete':
    #         check = USER.objects.get(user_id = user)
    #         salt=check.salt
    #         u_pw_db = USER.objects.get(user_id = request.POST.get('id')).pw # db에 저장된 암호화된 암호
    #         u_pw = hashlib.sha256(str(request.POST.get('pw')+salt).encode()).hexdigest() # 암호화된 암호

    #         if u_pw_db == u_pw:
    #             check.delete()
    #             auth_logout(request)
    #             data = {'status':'delete_T'}
    #             return JsonResponse(data)
    #         else:
    #             data = {'status':'delete_F'}
    #             return JsonResponse(data)
    #     else:
    #         data = {'status':'delete_F'}
    #         return JsonResponse(data)

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
        delete_log = request.POST.getlist('id[]')   
        for id in delete_log:
            delete = LOG.objects.get(log_id=id)
            delete.delete()
    return render(request, 'member/mypage.html', {'user':user, 'log_list':log_list, 'info':info, 'page_range' : range(start_page, end_page + 1), 'now_page': now_page})

def modify(request):
    return render(request, 'member/modify.html')

# user 출력
def user(request):
    user_list = USER.objects.all()
    return render(
        request,
        'member/line.html',
        {'user_list': user_list}
    )


#로그인
def login_custom(request):
    if request.method == 'POST':
        u_id = request.POST.get('user_id')
        u_pw = request.POST.get('user_pw')
        
        if 'rest_password' in request.POST:
            u_id = request.POST.get('user_id2')
            check = USER.objects.get(user_id = u_id)
            salt=check.salt
            pw_text = request.POST.get('rest_password')
            pw_text = hashlib.sha256(str(pw_text+salt).encode()).hexdigest()
            u_pw_db = USER.objects.get(user_id = u_id).pw
            if pw_text == u_pw_db:
                check.account_state = '활성계정'
                check.login_date = timezone.now()
                check.save()
                status = {'status' : 'rest_T'}
            else:
                status = {'status' : 'rest_F'}
            return JsonResponse(status)
        else:
            try:
                check = USER.objects.get(user_id = u_id)
                salt=check.salt
                u_pw=hashlib.sha256(str(u_pw+salt).encode()).hexdigest()
                user = USER.objects.get(user_id = u_id, pw = u_pw)
                if user.account_state == '휴면계정':
                    status = {'status' : 'rest', 'u_id':check.user_id}
                    print(status['u_id'])
                    return JsonResponse(status)
                user.login_date = timezone.now()
                user.save()
            except USER.DoesNotExist:
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
        _LENGTH = 28 # 몇자리? 
        string_pool = string.digits # "0123456789" 
        salt = "1" # 결과 값 
        for i in range(_LENGTH) : 
            # 랜덤한 하나의 숫자를 뽑아서, 문자열 결합을 한다. 
            salt += random.choice(string_pool) 

        # 날짜데이터 전처리
        data_list = b_date.split("-")
        b_year, b_month, b_day = data_list[0], data_list[1], data_list[2]
        
        # 휴대전화 유효성 검사
        phone_regex = re.compile("^(01)\d{1}-\d{3,4}-\d{4}$")
        phone_validation = phone_regex.search(p_num.replace(" ",""))
        
        
        # 이메일 유효성 검사
        mail_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        mail_validation = mail_regex.match(email)

        # 공란체크
        if (u_id=='') or (u_pw=='') or (u_name=='') or (b_date=='') or (p_num=='') or (email==''):
            data = {'status': 'empty_error'}
            return JsonResponse(data)

        if USER.objects.filter(user_id = u_id).exists():
            data = {'status': 'id_error'}
            return JsonResponse(data)    
        
        if USER.objects.filter(email = email).exists():
            data = {'status': 'sameemail_error'}
            return JsonResponse(data) 
        
        if (len(u_pw) < 8) or (len(u_pw) > 20):
            data = {'status': 'pw_len_error'}
            return JsonResponse(data) 
        
        if (u_pw != u_pw2):
            data = {'status':'pw_error'}
            return JsonResponse(data)
        
        if not mail_validation:
            data = {'status':'email_error'}
            return JsonResponse(data)
        
        if not phone_validation:
            data = {'status': 'phone_error'}
            return JsonResponse(data)
            
        u_pw=hashlib.sha256(str(u_pw+salt).encode()).hexdigest()

        u = USER(
            user_id=u_id, pw=u_pw, name=u_name, 
            birth_year=b_year,birth_month=b_month,birth_day=b_day, phone_num=p_num, email=email, salt=salt, usage_count=0, join_date=timezone.now())
        u.date_joined = timezone.now()
        u.save()

        data = {'status':'T'}
        return JsonResponse(data)

    else:
        return render(request, 'member/signup_custom.html')

def logout_custom(request):
    try:
        request.session['user_id']
        
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
        
        check = USER.objects.get(user_id = request.session['user_id'])
        salt=check.salt
        o_pw1=hashlib.sha256(str(o_pw+salt).encode()).hexdigest()

        user_inst = USER.objects.get(user_id=request.session['user_id'])

        # 기존 비밀번호, 새 비밀번호, 새 비밀번호 확인이 공란일 때 처리
        if (o_pw == '') or (n_pw == '') or (n_pw2 == ''):
            data = {'status':'empty_error'}
            return JsonResponse(data)
        
        # 새 비밀번호랑 새 비밀번호 확인이 다를 때 처리
        if (n_pw != n_pw2):
            data = {'status':'cofirm_error'}
            return JsonResponse(data)
        
        # 로그인한 아이디에 해당하는 user의 pw와 db속 패스워드가 다를 때 처리
        if (user_inst.pw != o_pw1):
            data = {'status':'pw_error'}
            return JsonResponse(data)

        # 새 비밀번호가 8~20자리가 아닐 경우 처리
        if not(len(n_pw) >= 8 and len(n_pw) <= 20) or not(len(n_pw2) >= 8 and len(n_pw2) <= 20) :
            data = {'status':'pw_len_error'}
            return JsonResponse(data)

        # 기존 비밀번호와 새 비밀번호가 같을 경우 처리
        if (o_pw == n_pw) or (o_pw == n_pw2):
            data = {'status' : 'same_pw_error'}
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
            request.session['user_id']
            return render(request, 'member/change_pw.html')
        except KeyError:
            return redirect('/need_login')
        

def change_info(request):
    
    if request.method == 'POST':
        user_id = request.session['user_id']
        user_inst = USER.objects.get(user_id=user_id)
        
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
            user_inst = USER.objects.get(user_id=user_id)
            name = user_inst.name
            email = user_inst.email
            phone_num = user_inst.phone_num
            return render(request, 'member/change_info.html',  {'name':name, 'email':email, 'phone_num':phone_num})
        except KeyError:
            return redirect('/need_login')     

def account_withdrawal(request):
    if request.method == "POST":
        o_pw = request.POST.get('origin_password')
        c_pw = request.POST.get('confirm_password')

        if (o_pw == '') or (c_pw == ''):
            data = {'status':'empty_error'}
            print(data)
            return JsonResponse(data)
        check = USER.objects.get(user_id = request.session['user_id'])
        salt=check.salt
        o_pw=hashlib.sha256(str(o_pw+salt).encode()).hexdigest()
        c_pw=hashlib.sha256(str(c_pw+salt).encode()).hexdigest()
        u_pw_db = check.pw

        if u_pw_db == o_pw and u_pw_db == c_pw:
            check.delete()
            auth_logout(request)
            data = {'status':'delete_T'}
            print(data)
            return JsonResponse(data)
        else:
            data = {'status':'delete_F'}
            print(data)
            return JsonResponse(data)
    else:
        try:
            request.session['user_id']
            return render(request, 'member/account_withdrawal.html')
        except KeyError:
            return redirect('/need_login')

# @method_decorator(logout_message_required, name='dispatch')
class RecoveryPwView(View):
    template_name = 'member/recovery_pw.html'
    recovery_pw = RecoveryPwForm

    def get(self, request):
        if request.method=='GET':
            form = self.recovery_pw(None)
            return render(request, self.template_name, {'form':form, })

def ajax_find_pw_view(request):
    user_id = request.POST.get('user_id')
    name = request.POST.get('name')
    email = request.POST.get('email')
    result_pw = USER.objects.get(user_id=user_id, name=name, email=email)
    request.session['auth'] = result_pw.user_id  

    # if result_pw:
    #     auth_num = email_auth_num()
    #     result_pw.auth = auth_num 
    #     result_pw.save()

    # send_mail(
    #     '비밀번호 찾기 인증메일입니다.',
    #     [email],
    #     html=render_to_string('member/recovery_email.html', {
    #         'auth_num': auth_num,
    #     }),
    # )
    return HttpResponse(json.dumps({"result": result_pw.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")

def auth_confirm_view(request):
    user_id = request.POST.get('user_id')
    input_auth_num = request.POST.get('input_auth_num')
    target_user = USER.objects.get(user_id=user_id, auth=input_auth_num)
    target_user.auth = ""
    target_user.save()
    request.session['auth'] = target_user.user_id  
    
    return HttpResponse(json.dumps({"result": target_user.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")

# @logout_message_required
def auth_pw_reset_view(request):
    # if request.method == 'GET':
    #     if not request.session.get('auth', False):
    #         raise PermissionDenied

    if request.method == 'POST':
        session_user = request.session['auth']
        user_inst=USER.objects.get(user_id=session_user)

        salt=user_inst.salt

        pw = request.POST.get('new_password2')
        pw=hashlib.sha256(str(pw+salt).encode()).hexdigest()

        reset_password_form = CustomSetPasswordForm(request.user, request.POST)
        

        if reset_password_form.is_valid():
            user_inst.pw = pw
            user_inst.save()
            # return redirect('/')
        else:
            request.session['auth'] = session_user
    else:
        reset_password_form = CustomSetPasswordForm(request.user)

    return render(request, 'member/password_reset.html', {'form':reset_password_form})




# @method_decorator(logout_message_required, name='dispatch')
class RecoveryIdView(View):
    template_name = 'member/recovery_id.html'
    recovery_id = RecoveryIdForm

    def get(self, request):
        if request.method=='GET':
            form = self.recovery_id(None)
        return render(request, self.template_name, {'form':form, })


def ajax_find_id_view(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    result_id = USER.objects.get(name=name, email=email)
    return HttpResponse(json.dumps({"result_id": result_id.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")

def information(request):
    #user_list = USER.objects.all()
    return render(
            request,
            'member/information.html')
