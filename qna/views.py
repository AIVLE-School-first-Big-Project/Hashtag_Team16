from django.shortcuts import render

from qna.models import *

# Create your views here.

def qna_board(request):
    qna_list = ARTICLE.objects.all()
    write_date_list = qna_list.order_by('-date')
    return render(request, 'qna/qna.html',{'write_date_list':  write_date_list})

def create(request):
    qna_list = ARTICLE.objects.all()
    write_date_list = qna_list.order_by('-date')
    return render(request, 'qna/create.html',{'write_date_list':  write_date_list})

#def index(request):
#    return render(request, 'qna/qna.html')
