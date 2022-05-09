from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

# Create your views here.
from .models import *

def index(request):
    #휴면계정
    u = USER.objects.all()
    for i in range(len(u)):
        # 마지막 로그인 날짜가 존재할 경우
        if (u[i].login_date is None): # 마지막 로그인 날짜가 존재하지 않을 경우 가입날짜로 판단
            if check_date_1year(u[i].join_date) == 'T':
                dormant_account = USER.objects.get(user_id = u[i].user_id)
                dormant_account.account_state = '휴면계정'
                dormant_account.save()
        else: # 마지막 로그인 날짜가 존재하는 경우
            if check_date_1year(u[i].login_date) == 'T':
                dormant_account = USER.objects.get(user_id = u[i].user_id)
                dormant_account.account_state = '휴면계정'
                dormant_account.save()


    return render(request, 'title/index.html')

def need_login(request):
    return render(request, 'title/need_login.html')


def check_date_1year(date):
    if (timezone.now() - date) >= timedelta(days = 365):
        return 'T'
    else:
        return 'F'