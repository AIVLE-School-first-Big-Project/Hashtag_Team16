from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import USER
from django.utils import timezone
from django.http import HttpResponse

# Create your views here.
from .models import USER

app_name = 'member'

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
    #user_list = USER.objects.all()
    if request.method == 'POST':
        u_id = request.POST.get('user_id')
        u_pw = request.POST.get('user_pw')

        try:
            user = USER.objects.get(user_id = u_id, pw = u_pw)
        except USER.DoesNotExist as e:
            return HttpResponse('로그인 실패')
        else:
            request.session['user_id'] = user.user_id
            request.session['user_name'] = user.name
        # 회원정보 조회 실패시 예외 발생
        
        return render(request, 'member/login_custom.html')
        #return redirect('member:login')
        #return redirect('index')
    else:
        return render(request, 'member/login_custom.html')

#회원가입
def signup_custom(request):
    if request.method == 'POST':
        u_id = request.POST.get('user_id')
        u_pw = request.POST.get('pw')
        u_name = request.POST.get('name')
        b_year = request.POST.get('birth_year')
        b_month = request.POST.get('birth_month')
        b_day = request.POST.get('birth_day')
        p_num = request.POST.get('phone_num')
        email = request.POST.get('email')

        u = USER(
            user_id=u_id, pw=u_pw, name=u_name, 
            birth_year=b_year,birth_month=b_month,birth_day=b_day, phone_num=p_num, email=email)
        u.date_joined = timezone.now()
        u.save()

        return HttpResponse(
                '가입 완료<br>%s %s %s' % (u_id, u_pw, u_name))
        #return redirect('../../')
    else:
        return render(request, 'member/signup_custom.html')

def logout_custom(request):
    del request.session['user_id']
    del request.session['user_name']

    request.session.flush()

    return render(request, 'member/login_custom.html')
