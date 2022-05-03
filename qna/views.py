from django.shortcuts import redirect, render
from django.utils import timezone
from qna.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Count
import json
import os
from google.cloud import storage
# Create your views here.
def image_func(): #storage 접근
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\User\\Downloads\\sample-347306-82fb108d9ea5.json"
    bucket_name = 'db_image'    # 서비스 계정 생성한 bucket 이름 입력
    source_file_name = 'C:\\Users\\User\\Desktop\\doggg.jpg'    # GCP에 업로드할 파일 절대경로
    destination_blob_name = 'dog'    # 업로드할 파일을 GCP에 저장할 때의 이름
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    return bucket_name

def qna_board(request):
    try:
        user = USER.objects.get(user_id = request.session['user_id']).user_id
        qna_list=ARTICLE.objects.all()
        if request.method == "POST":
            if request.POST.get('value')=='my_writing':#내가 쓴글 가져오기
                qna_list = ARTICLE.objects.filter(user=user)
                print(qna_list)
                print('test1')
                print(request.POST.get('value'))
                print(user)
                qna_list = qna_list[0]
                data = {'no':  qna_list.article_id, 'title':qna_list.title, 'user':qna_list.user.user_id, 'date':qna_list.date}
                
            return JsonResponse(data)

        else:
            print(qna_list)

            now_page = request.GET.get('page', 1)
            write_date_list = qna_list.order_by('-date')
            p = Paginator(write_date_list, 10)
            now_page = int(now_page)
            info = p.get_page(now_page)
            start_page = (now_page - 1) // 10 * 10 + 1
            end_page = start_page + 9
            if end_page > p.num_pages:
                end_page = p.num_pages
                
            ############comment##############
            data = (COMMENT.objects
                    .values('article_id')
                    .annotate(cnt_sum=Count('comment_id'))
                    .values('article_id','cnt_sum')
                    .order_by('-article_id'))
            
            cnt_comment = {}
            cnt = 1
            
            for i in write_date_list:
                # key = i.id
                #info
                try:
                    cnt_comment[cnt] = data.get(article_id = i.article_id)['cnt_sum']
                except:
                    cnt_comment[cnt] = 0
                cnt += 1
            #################################
                
            return render(request, 'qna/qna.html',{'write_date_list':  write_date_list, 'info' : info, 'page_range' : range(start_page, end_page + 1), 'user':user, 'cnt_comment':cnt_comment, 'key' : 2})
    
    except KeyError:
        return redirect('/need_login') 


def create(request):
    
    if request.method == 'POST':
        print('create')
        user = USER.objects.get(user_id=request.session['user_id']).user_id  
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
        try:
            user = USER.objects.get(user_id=request.session['user_id']).user_id
            return render(request, 'qna/create.html', {'user':user})
        except KeyError:
            return redirect('/need_login') 

def post(request, pk):
    try:
        user = USER.objects.get(user_id=request.session['user_id']).user_id  
        poster = ARTICLE.objects.get(article_id = pk)
        # com = COMMENT.objects.filter(article_id = pk)
        com = poster.comment_set.all()
        if request.method =='POST':
            if poster.user.user_id == user:
                poster.delete()
                data = {'status':'T'}
                return JsonResponse(data)
            else :
                data = {'status':'user_error'}
                return JsonResponse(data)
        
                
        p_title = poster.title
        p_content = poster.content

        return render(request, 'qna/post.html', {'p_title':p_title, 'p_content':p_content, 'article_id':pk, 'user':user,'comments': com})
    except KeyError:
        return redirect('/need_login') 



def p_modify(request, pk):
    al = ARTICLE.objects.get(article_id=pk)
    user = USER.objects.get(user_id = request.session['user_id']).user_id
    if request.method == 'POST':
        if al.user.user_id != request.session['user_id']:
            data = {'status':'user_error'}
            return JsonResponse(data)
        title = request.POST.get('title')
        content = request.POST.get('content')
        al.title = title
        al.content = content
        al.image ='123'
        
        if (al.title == '') or (al.content == ''):
            data = {'status':'F'}
            return JsonResponse(data)
        else:
            al.save()
            data = {'status':'T'}
            return JsonResponse(data) 
        
    else:
        try:
            user = USER.objects.get(user_id=request.session['user_id']).user_id  
            title = al.title
            content=al.content
            return render(request, 'qna/p_modify.html',  {'title':title, 'content':content, 'user':user, 'article_id':pk})
        except KeyError:
            return redirect('/need_login') 
        
def comment(request, pk):
    # 생성
    if request.POST.get('method') == 'C':
        comment = COMMENT(
            comment_id = COMMENT.objects.order_by('-comment_id').first().comment_id + 1,
            user = USER.objects.get(user_id=request.session['user_id']),
            content = request.POST.get('content'),
            date = timezone.now(),
            article =  ARTICLE.objects.get(article_id=pk)
            )
        if comment.content != '':
            comment.save()
            data = {'status':'create_T'}
            return JsonResponse(data)
        else:
            data = {'status':'create_F'}
            return JsonResponse(data)
    
    # 삭제
    else :
        id = request.POST.get('id')
        comment = COMMENT.objects.get(comment_id=id)
        if comment.user.user_id == request.session['user_id']:
            comment.delete()
            data = {'status':'delete_T'}
            return JsonResponse(data)
        else:
            data = {'status':'delete_F'}
            return JsonResponse(data)
    
    

