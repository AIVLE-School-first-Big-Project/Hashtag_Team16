#######################--NEED IMPORT--#########################
from django.shortcuts import render,redirect
from django.http import HttpResponse
from pytz import timezone
from qna.models import *
import os, datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from google.cloud import storage
from django.http import JsonResponse
import hashlib # image 저장할때 이름을 암호화하기 위함
import json
import requests
###############################################################

def index(request):
    # Login이 안된 상태에서는 연결하지 못하도록
    try:
        # 현재 로그인이 되어있는건지 test
        request.session['user_id']
        if request.method == 'POST':
            print('post')
            # 평점 스코어, 피드백 내용 기능 구현
            if 'score' in request.POST:
                #log = LOG.objects.get(l_user_id = request.session['user_id'])
                log1 = LOG.objects.create(
                    log_id = LOG.objects.order_by('-log_id').first().log_id + 1,
                    user = USER.objects.get(user_id=request.session['user_id']),
                    service_score = request.POST.get('score'),
                    feedback = request.POST.get('feedback'),
                    image = None,
                    prior_tag = '#pig',
                    after_tag = '#pig'
                )
     
                if (log1.service_score == '') or (log1.feedback == ''):
                    data = {'status':'F'}
                    return JsonResponse(data)
                else:
                    log1.save()
                    data = {'status':'T'}
                    return JsonResponse(data)
            
            
            
            data = request.FILES['attachedImage']                                       # 1. 이미지를 브라우저로부터 받아옵니다.
            image_name, time = str(data), str(datetime.datetime.now())                  # 2. 이미지 이름과 현재 시간을 문자열로 저장합니다
            extension = '.' + image_name.split('.')[-1]                                       # 3. 이미지 이름에 확장자를 따로 변수에 저장합니다.
            tmp_name = image_name + time                                                # 4. 두 문자열을 합한 str 객체 생성
            secret_name = hashlib.sha256(tmp_name.encode()).hexdigest() + extension     # 5. str객체를 sha256방식으로 암호화 시킨다.(확장자를 붙여준다.)
                                                                                        #    --> 중복되는 이름이 GCP에 저장되는 것을 방지하기 위한 방식입니다. 또한 스토리지에 url로 접근이 가능하기 때문에,
                                                                                        #        파일 이름을 모르게 하는 것이 보안에 도움이 됩니다. 이렇게 저장이 될 경우 파일의 원래 이름은 서버관리자도 알 수 없습니다.
            path = default_storage.save(secret_name, ContentFile(data.read()))          # 5. 암호화된 이름으로 이미지 서버(로컬)에 저장
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)                          # 6. 저장된 이미지의 절대 경로         
            
            # 해쉬태그 생성 API
            files = open(tmp_file, 'rb')
            upload = {'file': files}
            res = requests.post(' http://118.91.69.43:5000/', files = upload)
            hashtags_json = json.loads(res.content)
            print(type(hashtags_json))
            print(hashtags_json)
            files.close()
            

            
            ## LOG 데이터 저장하기
            log = LOG.objects.create(
                log_id = LOG.objects.order_by('-log_id').first().log_id + 1,
                user = USER.objects.get(user_id=request.session['user_id']),
                service_score = None,
                feedback = None,
                image = image_func(tmp_file, secret_name),  # 이미지를 GCP에 올린 후 GCP에서 읽어올 수 있는 경로 저장함( 함수정의 맨 아래 )
                prior_tag = '#pig',
                after_tag = '#pig'
            )

            os.remove(tmp_file) # 이미지 삭제

            if (tmp_file == ''):
                data = {'status':'F'}
                return JsonResponse(data)
            
            log.save()
            
            data = {'status':'T'}
            return JsonResponse(data)
        else:
            user = USER.objects.get(user_id=request.session['user_id']).user_id
            return render(request, 'main/index.html', {'user' : user})
    except KeyError:
        
        return redirect('/need_login')

def function(request):
    try:
        user = USER.objects.get(user_id=request.session['user_id']).user_id                

        return render(request, 'main/function.html', {'user' : user})
    except KeyError:
        return redirect('/need_login')


################GCP 파일 업로드#################################
def image_func(tmp_file, image_name):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "static/sample-347306-82fb108d9ea5.json"
    bucket_name = 'db_image'                        # 서비스 계정 생성한 bucket 이름 입력
    source_file_name = tmp_file                     # GCP에 업로드할 파일 절대경로
    destination_blob_name = image_name              # 업로드할 파일을 GCP에 저장할 때의 이름
    storage_client = storage.Client()               #
    bucket = storage_client.bucket(bucket_name)     #
    blob = bucket.blob(destination_blob_name)       #   
    blob.upload_from_filename(source_file_name)     #
    return 'https://storage.googleapis.com/db_image/' + image_name


##################해시태그 게시글 수 크롤링######################
def hashtag_cnt_crawling(target):
    # import requests
    url = 'https://www.instagram.com/explore/tags/'+ target +'/?__a=1&__d=dis'
    response = requests.get(url)
    cnt = response.json()['graphql']['hashtag']['edge_hashtag_to_media']['count']
    return cnt