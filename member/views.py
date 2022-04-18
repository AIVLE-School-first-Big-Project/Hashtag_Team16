from django.shortcuts import render, redirect

# Create your views here.
from .models import USER

app_name = 'member'
# Create your views here.
def login_custom(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_pw = request.POST.get('user_pw')

        user = USER.objects.get(user_id = user_id, user_pw = user_pw)
        # 회원정보 조회 실패시 예외 발생
        #return redirect('member:login')
        return redirect('index')
    else:
        return render(request, 'member/login_custom.html')

        
from .models import USER
from django.utils import timezone
from django.http import HttpResponse
def signup_custom(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_pw = request.POST.get('user_pw')
        user_name = request.POST.get('user_name')
        m = Member(
        user_id=user_id, user_pw=user_pw, user_name=user_name)
        m.date_joined = timezone.now()
        m.save()
        return HttpResponse(
            '가입 완료<br>%s %s %s' % (user_id, user_pw, user_name))
    else:
         return render(request, 'member/signup_custom.html')
