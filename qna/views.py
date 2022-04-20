from django.shortcuts import redirect, render
from django.utils import timezone
from qna.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
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


def create(request, pk):  
    if request.method == 'POST':
        print('save0')
        article = ARTICLE(
            #article_id = ARTICLE.objects.filter(article_id = pk)[0] ,
            article_id = 5,
            board = BOARD.objects.get(board_name='qna게시판'),
            #a_user_id=USER.objects.get(u_id=request.session['u_id']),
            user = USER.objects.get(user_id='hw'),
            title = request.POST.get('title'),
            content = request.POST.get('content'),
            date = timezone.now(),
            image = None,
            comment_cnt = 0
            )
        article.save()
        print('save1')
        data = {'status':True}
        data =  json.dumps(data)
        return JsonResponse(data, safe=False)
    else:
        print("save2")
        return render(request, 'qna/create.html')

def post(request):
    return render(request, 'qna/post.html')

#def index(request):
#    return render(request, 'qna/qna.html')
