from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .models import USER

app_name = 'member'
# Create your views here.
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
            #request.session['user_name'] = user.name
        # 회원정보 조회 실패시 예외 발생
        
        return render(request, 'member/login_custom.html')
        #return redirect('index')
    else:
        return render(request, 'member/login_custom.html')
