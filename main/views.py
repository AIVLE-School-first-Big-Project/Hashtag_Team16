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
            res = requests.post(' http://192.168.137.1:5002/', files = upload)
            hashtags_json = json.loads(res.content)
            files.close()
            
            # best 해시태그 만들기
            output_json = {i: hashtag_cnt_crawling(i[1:]) for i in hashtags_json['hashtags'][:5]}
            hashtags_json['best_hashtag'] = output_json
            
            # list 문자열로 변환
            result = ' '.join(s for s in hashtags_json['hashtags'])

            ## LOG 데이터 저장하기
            log = LOG.objects.create(
                
                log_id = LOG.objects.order_by('-log_id').first().log_id + 1,
                user = USER.objects.get(user_id=request.session['user_id']),
                service_score = None,
                feedback = None,
                image = image_func(tmp_file, secret_name),  # 이미지를 GCP에 올린 후 GCP에서 읽어올 수 있는 경로 저장함( 함수정의 맨 아래 )
                prior_tag = result
            )
            os.remove(tmp_file) # 이미지 삭제

            if (tmp_file == ''):
                data = {'status':'F'}
                return JsonResponse(data)
            

            log.save()
            data = {'status':'T', 'hashtags': hashtags_json['hashtags'], 'best_hashtag': hashtags_json['best_hashtag'] , 
            'img1':hashtags_json['img1'], 'img2':hashtags_json['img2'], 'img3':hashtags_json['img3'], 'img4':hashtags_json['img4'] }
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
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "static/bigpro-349004-9d5cfb49c746.json"
    bucket_name = 'db_image2'                        # 서비스 계정 생성한 bucket 이름 입력
    source_file_name = tmp_file                     # GCP에 업로드할 파일 절대경로
    destination_blob_name = image_name              # 업로드할 파일을 GCP에 저장할 때의 이름
    storage_client = storage.Client()               #
    bucket = storage_client.bucket(bucket_name)     #
    blob = bucket.blob(destination_blob_name)       #   
    blob.upload_from_filename(source_file_name)     #
    return 'https://storage.googleapis.com/db_image2/' + image_name


##################해시태그 게시글 수 크롤링######################
def hashtag_cnt_crawling(target):
    url = 'https://www.instagram.com/explore/tags/'+ target +'/?__a=1&__d=dis'
    
    try:
        request_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'mid=YlYfjwALAAEvqHbHUXULJQJq7qQn; ig_did=343A39EB-4F06-4541-BCC2-DC048E972F3E; ig_nrcb=1; datr=nx9WYpcVM-Icm4CjPMZgINXd; shbid="9028\0545810238458\0541683176261:01f7a2af08c8917ecd8f0b842c0ffe9d1b9892b38ebe9657ce0cdb5ba3510d791a781fb0"; shbts="1651640261\0545810238458\0541683176261:01f7ea888175c8e87d1381ae8e2d84b0d91062ffba393d2a5c4127896f46aacc73baaa87"; csrftoken=IGJ6YetFdUrZQESMiueiWCoJMd5gNV3e; ds_user_id=53290782834; sessionid=53290782834%3A3n8XlfwshDz9bA%3A15; rur="VLL\05453290782834\0541683275516:01f7c7997ceaa181318792a62d682729ae9b66000135e25190ecdb4be1e67452bac0b5e2"'
            } 
        response = requests.get(url,headers = request_headers)
        cnt = response.json()['data']['media_count']
    except:
        response = requests.get(url)
        cnt = response.json()['graphql']['hashtag']['edge_hashtag_to_media']['count']
        
    return cnt