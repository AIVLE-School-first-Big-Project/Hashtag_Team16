from django.shortcuts import render,redirect
from django.http import HttpResponse
from qna.models import *

def index(request):
    # Login이 안된 상태에서는 연결하지 못하도록
    user = USER.objects.get(user_id=request.session['user_id']).user_id
    try:                
        request.session['user_id']
        return render(request, 'main/index.html', {'user' : user})
    except KeyError:
        return redirect('/')

    