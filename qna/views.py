from django.shortcuts import redirect, render
from django.utils import timezone
from qna.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
# Create your views here.

def qna_board(request):
    user = USER.objects.get(user_id=request.session['user_id']).user_id
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
    
        
    return render(request, 'qna/qna.html',{'write_date_list':  write_date_list, 'info' : info, 'page_range' : range(start_page, end_page + 1), 'user':user})


def create(request):
    user = USER.objects.get(user_id=request.session['user_id']).user_id  
    if request.method == 'POST':
        print(ARTICLE.objects.order_by('-article_id').first().article_id)
        
        article = ARTICLE(
            #article_id = ARTICLE.objects.filter(article_id = pk)[0] ,
            article_id = ARTICLE.objects.order_by('-article_id').first().article_id + 1,
            board = BOARD.objects.get(board_name='qna게시판'),
            #a_user_id=USER.objects.get(u_id=request.session['u_id']),
            user = USER.objects.get(user_id=request.session['user_id']),
            # user = request.session['user_id'],
            title = request.POST.get('title'),
            content = request.POST.get('content'),
            date = timezone.now(),
            image = None,
            comment_cnt = 0
            )
        print(article.content)
        if (article.content == '') or (article.title == ''):
            data = {'status':'F'}
            return JsonResponse(data)
        
        article.save()
        data = {'status':'T'}
        return JsonResponse(data)
    else:
        return render(request, 'qna/create.html', {'user':user})

def post(request, pk):
    user = USER.objects.get(user_id=request.session['user_id']).user_id  
    poster = ARTICLE.objects.get(article_id = pk)
    
    if request.method =='POST':
        if request.POST.get('cancel') == "삭제":
            poster.delete()
            return redirect('http://127.0.0.1:8000/qna')
        elif request.POST.get('update') == '수정':
            p_title = poster.title
            p_content = poster.content
            return render(request, 'qna/p_modify.html',{'p_title':p_title, 'p_content':p_content, 'user':user})
        else:
            if (poster.content == '') or (poster.title == ''):
                data = {'status':'F'}
                return JsonResponse(data)
            else:
                poster.save()
                data = {'status':'T'}
                return JsonResponse(data)
    p_title = poster.title
    p_content = poster.content

    return render(request, 'qna/post.html', {'p_title':p_title, 'p_content':p_content, 'article_id':pk, 'user':user})

def logout_custom(request):
    del request.session['user_id']
    del request.session['user_name']

    request.session.flush()

    return redirect('/')

# def update(request):
    
#     article = ARTICLE(
#         article_id = ARTICLE.objects.get(user_id='hw').article_id,
#         board = BOARD.objects.get(board_name='qna게시판'),
#         #user = USER.objects.get(user_id=request.session['user_id']),
#         user = USER.objects.get(user_id='hw'),
#         title = request.POST.get('title'),
#         content = request.POST.get('content'),
#         date = timezone.now(),
#         image = None,
#         comment_cnt = 0
#         )
#     article.save()

#     return render(request, 'qna/post.html')

def p_modify(request):
    return render(request, 'qna/p_modify.html')


#def index(request):
#    return render(request, 'qna/qna.html')
