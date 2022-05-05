#######################--NEED IMPORT--#########################
from django.shortcuts import render,redirect
from django.views import View
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
from multiprocessing import Pool
###############################################################

def index(request):
    # Login이 안된 상태에서는 연결하지 못하도록
    try:
        # 현재 로그인이 되어있는건지 test
        request.session['user_id']
        if request.method == 'POST':
            # 해쉬태그 생성 API
            files = open(tmp_file, 'rb')
            upload = {'file': files}
            res = requests.post('http://192.168.137.1:5002/', files = upload)
            hashtags_json = json.loads(res.content)


            files.close()
            
            # best 해시태그 만들기
            
            
            # 평균 좋아요
            likes_json = hashtag_likes_crawling(hashtags_json['hashtags'][0][1:])
            hashtags_json['likes_hashtag'] = likes_json

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
            data = {'status':'T', 'hashtags': hashtags_json['hashtags'], 'best_hashtag': hashtags_json['best_hashtag'] ,  'likes_hashtag':hashtags_json['likes_hashtag'], 
            'img1':hashtags_json['img1'], 'img2':hashtags_json['img2'], 'img3':hashtags_json['img3'], 'img4':hashtags_json['img4'] }
            return JsonResponse(data)
            
        else:
            user = USER.objects.get(user_id=request.session['user_id']).user_id
            return render(request, 'main/index.html', {'user' : user})
    except KeyError:
        return redirect('/need_login')
    
class hashtag(View):
    def post(self, request):
        url = request.POST['url']
        # 해쉬태그 생성 API
        files = open(url, 'rb')
        upload = {'file': files}
        res = requests.post(' http://192.168.137.1:5001/hashtags20/', files = upload)
        hashtags_json = json.loads(res.content)
        files.close()
        os.remove(url)
        data = {'hashtag' : hashtags_json['hashtags']};



        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=4) as pool:
            print(pool.map(self.hashtag_cnt_crawling, hashtags_json['hashtags'][:5]))


        print(hashtags_json['hashtags'][:5])
        pool = Pool(4)
        squares = pool.map(hashtag_cnt_crawling, hashtags_json['hashtags'][:5]) 
        print(squares)
        
        return JsonResponse(data);

class image_upload_save(View):
    def post(self, request):
        data = request.FILES['attachedImage']                                       # 1. 이미지를 브라우저로부터 받아옵니다.
        image_name, time = str(data), str(datetime.datetime.now())                  # 2. 이미지 이름과 현재 시간을 문자열로 저장합니다
        extension = '.' + image_name.split('.')[-1]                                       # 3. 이미지 이름에 확장자를 따로 변수에 저장합니다.
        tmp_name = image_name + time                                                # 4. 두 문자열을 합한 str 객체 생성
        secret_name = hashlib.sha256(tmp_name.encode()).hexdigest() + extension     # 5. str객체를 sha256방식으로 암호화 시킨다.(확장자를 붙여준다.)
                                                                                    #    --> 중복되는 이름이 GCP에 저장되는 것을 방지하기 위한 방식입니다. 또한 스토리지에 url로 접근이 가능하기 때문에,
                                                                                    #        파일 이름을 모르게 하는 것이 보안에 도움이 됩니다. 이렇게 저장이 될 경우 파일의 원래 이름은 서버관리자도 알 수 없습니다.
        path = default_storage.save(secret_name, ContentFile(data.read()))          # 5. 암호화된 이름으로 이미지 서버(로컬)에 저장
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)                          # 6. 저장된 이미지의 절대 경로
        data = {'url' : image_func(tmp_file, secret_name), 'l_url' : tmp_file};
        
        return JsonResponse(data);

    
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
    storage_client = storage.Client()               #
    bucket = storage_client.bucket(bucket_name)     #
    blob = bucket.blob(destination_blob_name)       #   
    blob.upload_from_filename(source_file_name)     #
    return 'https://storage.googleapis.com/db_image2/' + image_name


##################해시태그 게시글 수 크롤링######################
def hashtag_cnt_crawling(self, target):
    url = 'https://www.instagram.com/explore/tags/'+ target +'/?__a=1&__d=dis'
    try:
        request_headers = {
            'cookie': 'ig_did=9218D585-1D45-43F2-8CD8-551A16853932; ig_nrcb=1; mid=YmwBYAALAAH-JdcTDWyYG3JrAfjD; fbm_124024574287414=base_domain=.instagram.com; datr=BF5tYmZtnVsJotuwxMLxEXCS; shbid="11862\0541994601200\0541683075730:01f73c42489b8d6f5ee1f821a6aad3eeb95f5cf1b997832aa7aefcb86c45ef5885a25d9f"; shbts="1651539730\0541994601200\0541683075730:01f72f006f5f41b9af5b62a6d9f36cdb6b0c4cc89564cd99752f25f70597f1ed97fffce7"; csrftoken=lF08QydrVyuCWNssIa4HCJ5gRpSGsiF6; ds_user_id=1994601200; sessionid=1994601200%3AbHVDMgen5K46Ph%3A29; fbsr_124024574287414=o1UVaSf7ZKz-klW0FCWZwzhJJUvU2OQVL86LZy8bMAQ.eyJ1c2VyX2lkIjoiMTAwMDAzMjU2MDc3NDUzIiwiY29kZSI6IkFRQUFKYVlsU1dFb21VQnF1ZXdKdkVsOVY5RElxajV2aTE3SFFKNXJ2cnhhVGhmQzlMNjJFRFlGd1FYampUYjg0UUt2VDFiN0ktcGRmU1J1V0lPTFhqOU9KVUhqR2NFeVAyMEMtWVhPNWU1VFh3NF9WZWE5U3B5Q0dPLVdKYkxUZDVQdGRNeWNqWFJ6WFZOc0dfVGZsT09BOXpTajk4emZDOVpCQkxobnU1cEFiMkFfRjA5T0JzQUVhbk1aMG9qcDdWeWY2eHRPdVdnVS1vbGt6TjV2OFJ0eExXZ19mYzBYdUV1NUJhWmdaWTMtaTdNWlBCRUJmUEpYZE1maGx4YkRoWkEwMDhXMnZQS2ZBMHB6UlVrUHBZZ2s0M1hsbTRvcmdLZVFUOWFzcUlDUDFtREV1OF9NazJNNEpaVWNkYXZ4UkQ3YmU5bDFNVG4zUHJ0SXl4aHZHSjdXIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUtMMkJ5N2I3clhkTmVUbkJIMGNaQ3dYWkNneTZwWHA4SDRwdDN2SE1RWkF1TEYyTGJQeEppUUhVOHhBQVI0aVltVlpCYTM2ZEpoZVFaQWZsNnVJbEdnZmJFY3h2cWREOGZOSzgwTnJaQVJHd1JaQnRiMjlaQ01YZ3RQSnFIRmpmeFpDcTNHNkRXeHd3eFBZeHc1c1k5Vnp3VVNMRTZNUWZqRmpVQ0hvR1IyVk9YeDduUlpCUmRrbVFaRCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNjUxNzQwMDAyfQ; rur="VLL\0541994601200\0541683276024:01f7a867559c84d4d4716bf608c3fc46112b7570755b15ce466f54316efd0bdd77638b11"'
            } 
        response = requests.get(url ,headers = request_headers)
        cnt = response.json()['data']['media_count']
        return {target : cnt}
    except:
        response = requests.get(url)
        cnt = response.json()['graphql']['hashtag']['edge_hashtag_to_media']['count']
        return {target : cnt}
