from django.shortcuts import render

from qna.models import *
from django.core.paginator import Paginator

# Create your views here.

def qna_board(request):
    now_page = request.GET.get('page', 1)
    qna_list = ARTICLE.objects.all()
    write_date_list = qna_list.order_by('-date')
    p = Paginator(write_date_list, 10)
    now_page = int(now_page)
    info = p.get_page(now_page)
    start_page = (now_page - 1) // 10 * 10 + 1
    end_page = start_page + 9
    if end_page > p.num_pages:
        end_page = p.num_pages

        
    return render(request, 'qna/qna.html',{'write_date_list':  write_date_list, 'info' : info, 'page_range' : range(start_page, end_page + 1)})


def create(request):
    return render(request, 'qna/create.html')

def post(request):
    return render(request, 'qna/post.html')

#def index(request):
#    return render(request, 'qna/qna.html')
