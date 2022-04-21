from django.shortcuts import render,redirect
from django.http import HttpResponse

def index(request):
    # Login이 안된 상태에서는 연결하지 못하도록
    try:                
        request.session['user_id']
        return render(request, 'main/index.html')
    except KeyError:
        return redirect('/')
    