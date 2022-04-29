from django.shortcuts import render,redirect
from django.http import HttpResponse
from qna.models import *
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from google.cloud import storage
from django.http import JsonResponse
from PIL import Image
import joblib
# from pyspark.sql import SparkSession
# from pyspark.ml.recommendation import ALS, ALSModel

def index(request):
    # Login이 안된 상태에서는 연결하지 못하도록
    try:
        # 현재 로그인이 되어있는건지 test
        request.session['user_id']
        if request.method == 'POST':
            data = request.FILES['attachedImage']       # 이미지 request
            i_name = str(data)                          # 이미지 이름 저장
            path = default_storage.save(i_name, ContentFile(data.read()))   # 이미지 서버(로컬)에 저장
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)              # 저장된 이미지의 절대 경로         
            
            '''##################################log database save##############
            log = LOG.objects.create(
                log_id = LOG.objects.order_by('-log_id').first().log_id + 1,
                user = USER.objects.get(user_id=request.session['user_id']),
                service_score = None,
                feedback = None,
                image = image_func(url, real_file_name),
                prior_tag = '#pig',
                after_tag = '#pig'
            )
            if (url == ''):
                data = {'status':'F'}
                return JsonResponse(data)
            log.save()
            #################################################################'''
            
            ################GCP 파일 업로드#################################
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "static/sample-347306-82fb108d9ea5.json"
            bucket_name = 'db_image'                        # 서비스 계정 생성한 bucket 이름 입력
            source_file_name = tmp_file                     # GCP에 업로드할 파일 절대경로
            destination_blob_name = i_name                  # 업로드할 파일을 GCP에 저장할 때의 이름
            storage_client = storage.Client()               #
            bucket = storage_client.bucket(bucket_name)     #
            blob = bucket.blob(destination_blob_name)       #   
            blob.upload_from_filename(source_file_name)     #
            ################################################################
            
            os.remove(tmp_file) # 이미지 삭제
            
            
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

    
#

def image_func(url, real_file_name): #storage 접근
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\User\\Downloads\\sample-347306-82fb108d9ea5.json" #storage에 접근할 수 있는 json파일(일종의 고유한 key)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "static/sample-347306-82fb108d9ea5.json"
    bucket_name = 'db_image'    # 서비스 계정 생성한 bucket 이름 입력
    source_file_name = url   # GCP에 업로드할 파일 절대경로
    destination_blob_name = real_file_name    # 업로드할 파일을 GCP에 저장할 때의 이름
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    return url


def star(request):
    return render(request, 'main/star.html')

