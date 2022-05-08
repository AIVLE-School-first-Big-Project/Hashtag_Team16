#######################--NEED IMPORT--#########################
from django.shortcuts import render,redirect
from django.views import View
from qna.models import LOG, USER
import os
import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from google.cloud import storage
from django.http import JsonResponse
import hashlib # image 저장할때 이름을 암호화하기 위함
import json
import requests
import mp_module

###############################################################

class index(View):
    def get(self, request):
        # Login이 안된 상태에서는 연결하지 못하도록
        try:
            # 현재 로그인이 되어있는건지 test
            request.session['user_id']
            user = USER.objects.get(user_id=request.session['user_id']).user_id
            return render(request, 'main/index.html', {'user' : user})
        except KeyError:
            return redirect('/need_login')
    
    def post(self, request):
        url = request.POST['url']
        os.remove(url)
        tag = request.POST['tag']
        tag_string = ' '.join(s for s in tag)
        log = LOG.objects.create(
                log_id = LOG.objects.order_by('-log_id').first().log_id + 1,
                user = USER.objects.get(user_id=request.session['user_id']),
                service_score = None,
                feedback = None,
                image = request.POST['url2'],  # 이미지를 GCP에 올린 후 GCP에서 읽어올 수 있는 경로 저장함( 함수정의 맨 아래 )
                prior_tag = tag_string
            )
        log.save()
        data = {'status': 'success'}
        return JsonResponse(data)

class likes(View):
    def post(self, request):
        tags = request.POST['tags']
        tags = tags.split(',')
        data = {'like' : mp_module.hashtag_likes_crawling(tags[0][1:])}
        return JsonResponse(data)

class influence(View):
    def post(self, request):
        tags = request.POST['tags']
        tags = tags.split(',')
        data = {'influence' : mp_module.hashtag_influ_crawling(tags[0][1:])}
        return JsonResponse(data)

class GAN_image(View):
    def post(self, request):
        url = request.POST['url']
        files = open(url, 'rb')
        upload = {'file': files}
        res = requests.post('http://118.91.69.43:60002/styleimages4/', files = upload)
        hashtags_json = json.loads(res.content)
        files.close()
        data = {'img1':hashtags_json['img1'], 'img2':hashtags_json['img2'], 'img3':hashtags_json['img3'], 'img4':hashtags_json['img4']}
        return JsonResponse(data)

class hashtag(View):
    def post(self, request):
        url = request.POST['url']
        # 해쉬태그 생성 API
        files = open(url, 'rb')
        upload = {'file': files}
        res = requests.post('http://118.91.69.43:60001/hashtags20/', files = upload)
        hashtags_json = json.loads(res.content)
        files.close()

        
        data = {'hashtag' : hashtags_json['hashtags']}
        tag_dict, influ, like = mp_module.mult_process_tag(hashtags_json['hashtags'][:6])
        tag_dict = sorted(tag_dict.items(), key=lambda x: -x[1]) 
        tag_dict = {a:b for a,b in tag_dict}
        data['best_hash'] = tag_dict
        data['influence'] = influ
        data['like'] = like

        return JsonResponse(data)

class image_upload_save(View):
    '''
    1. 이미지를 브라우저로부터 받아옵니다.
    2. 이미지 이름과 현재 시간을 문자열로 저장합니다
    3. 이미지 이름에 확장자를 따로 변수에 저장합니다.
    4. 두 문자열을 합한 str 객체 생성
    5. str객체를 sha256방식으로 암호화 시킨다.(확장자를 붙여준다.)
    파일 이름을 모르게 하는 것이 보안에 도움이 됩니다. 이렇게 저장이 될 경우 파일의 원래 이름은 서버관리자도 알 수 없습니다.
    6. 암호화된 이름으로 이미지 서버(로컬)에 저장
    7. 저장된 이미지의 절대 경로
    '''
    def post(self, request):
        data = request.FILES['attachedImage']                                       
        image_name, time = str(data), str(datetime.datetime.now())                  
        extension = '.' + image_name.split('.')[-1]                                       
        tmp_name = image_name + time                                                
        secret_name = hashlib.sha256(tmp_name.encode()).hexdigest() + extension     
        path = default_storage.save(secret_name, ContentFile(data.read()))          
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)                          
        data = {'url' : image_func(tmp_file, secret_name), 'l_url' : tmp_file}
        return JsonResponse(data)

class function(View):
    def get(self, request):
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
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    return 'https://storage.googleapis.com/db_image2/' + image_name
