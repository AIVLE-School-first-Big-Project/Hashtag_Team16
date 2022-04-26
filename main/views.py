from django.shortcuts import render,redirect
from django.http import HttpResponse
from qna.models import *

def index(request):
    try:
        user = USER.objects.get(user_id=request.session['user_id']).user_id
        request.session['user_id']
        return render(request, 'main/index.html', {'user' : user})
    except KeyError:
        
        return redirect('/need_login')

def function(request):
    try:
        user = USER.objects.get(user_id=request.session['user_id']).user_id                

        return render(request, 'main/function.html', {'user' : user})
    except KeyError:
        return redirect('/need_login')

