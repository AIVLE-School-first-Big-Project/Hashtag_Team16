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
            res = requests.post('http://118.91.69.43:5002/', files = upload)
            hashtags_json = json.loads(res.content)


            files.close()
            
            # best 해시태그 만들기
            output_json = {i: hashtag_cnt_crawling(i[1:]) for i in hashtags_json['hashtags'][:5]}
            hashtags_json['best_hashtag'] = output_json
            
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
            'cookie': 'mid=YlTkmwALAAG8_hwvjoIMJQK68cpC; ig_did=7F40C175-A233-4640-BCA4-41546EB3533D; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; dpr=1.25; datr=azRyYqr5KFpgjE009pBFeTyu; shbid="478\05453094873418\0541683262590:01f7abf35b9b15790afd6da1998c0a6c04b516de37658e4c94b19682388a62e31eb9c790"; shbts="1651726590\05453094873418\0541683262590:01f73fe05d535571e3b520d284d9724ba0f892c957e7b1f733636cdd0421d553099be456"; fbsr_124024574287414=x8BX7TobCGuoo8ZLLOTF7YORu6dzdB8kc99QpUWD3kU.eyJ1c2VyX2lkIjoiMTAwMDA0MzIyNDA2NTgzIiwiY29kZSI6IkFRQXhrM21QM1UtRE8zUk9yWU1BZWF4U0FFaFUxRDhXcHU3TnVYMWZzRm9vbnYzalFSV1B1dkJtRjhVTldfOVAtZ21YSFJjTHU3dUU0Um9DTVZwWko1U2I4MzdYcEhhU3RTOXE1ckxEbXFoaG9MRzBWSmludHItaWpYVXptNEZVOHpteHlNck05SXFwVWduZDRmXzV3a0Nrcktma01hd3VpTm95ZEFIQnczOG5MS2drQU53OVZScm9ucE1pUUZicjQyVVRjal9uWnRUVG52OXUyZzU1TnZIdDYtTm45YVA1NkVSV1hyNlA4QTVjeFRuZF8ycktDeUVubWZXRjJvMFFnRk12MVBaallCZkxuWENjTDA0RlN5ZGhqTmFrWUh4RzkyTjZWN3Jxc2dwSUo3OEI0d1E2emg2S3V3cGI4bFZFbEg1UXYxNzRSTGowTjNNZkJWZjk1NzNTIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUlBMnJrZEFLV2N6aVRJWVhiOXowR1dNcWRaQ1Y3MVpCNVpDNjhLcDBaQmRaQnRpZTVmWXpoMWE4ZTh2SzFlU0FXTGhIYU1jNzRFMHpkcHM2M1ByNnJwTFRaQWI3bEFQNjFPYUVlSWM3dTBwMHNOT1ZNOWVuanVLY3BzS3ozdXhjN0VmVEJ4NlhUekVhalhMWGdUSnZVVGY5ckd5anJkRkdQVGg2OXpTc2giLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTY1MTczNzYzN30; csrftoken=h2w9VIoMkD1x35S5C7oa38RoUEYW01wa; ds_user_id=2955836353; sessionid=2955836353%3AZ4ICKx8RLE2LV9%3A27; fbsr_124024574287414=x8BX7TobCGuoo8ZLLOTF7YORu6dzdB8kc99QpUWD3kU.eyJ1c2VyX2lkIjoiMTAwMDA0MzIyNDA2NTgzIiwiY29kZSI6IkFRQXhrM21QM1UtRE8zUk9yWU1BZWF4U0FFaFUxRDhXcHU3TnVYMWZzRm9vbnYzalFSV1B1dkJtRjhVTldfOVAtZ21YSFJjTHU3dUU0Um9DTVZwWko1U2I4MzdYcEhhU3RTOXE1ckxEbXFoaG9MRzBWSmludHItaWpYVXptNEZVOHpteHlNck05SXFwVWduZDRmXzV3a0Nrcktma01hd3VpTm95ZEFIQnczOG5MS2drQU53OVZScm9ucE1pUUZicjQyVVRjal9uWnRUVG52OXUyZzU1TnZIdDYtTm45YVA1NkVSV1hyNlA4QTVjeFRuZF8ycktDeUVubWZXRjJvMFFnRk12MVBaallCZkxuWENjTDA0RlN5ZGhqTmFrWUh4RzkyTjZWN3Jxc2dwSUo3OEI0d1E2emg2S3V3cGI4bFZFbEg1UXYxNzRSTGowTjNNZkJWZjk1NzNTIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUlBMnJrZEFLV2N6aVRJWVhiOXowR1dNcWRaQ1Y3MVpCNVpDNjhLcDBaQmRaQnRpZTVmWXpoMWE4ZTh2SzFlU0FXTGhIYU1jNzRFMHpkcHM2M1ByNnJwTFRaQWI3bEFQNjFPYUVlSWM3dTBwMHNOT1ZNOWVuanVLY3BzS3ozdXhjN0VmVEJ4NlhUekVhalhMWGdUSnZVVGY5ckd5anJkRkdQVGg2OXpTc2giLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTY1MTczNzYzN30; rur="EAG\0542955836353\0541683273780:01f73d7e5918b65f996f161cfe89d74883fbd22b8deba334c47b654d04602996b01334d5"'
            } 
        response = requests.get(url,headers = request_headers)
        cnt = response.json()['data']['media_count']
    except:
        response = requests.get(url)
        cnt = response.json()['graphql']['hashtag']['edge_hashtag_to_media']['count']
        
    return cnt

def hashtag_likes_crawling(target):
    # import requests
    url = 'https://www.instagram.com/explore/tags/'+ target +'/?__a=1&__d=dis'
    try:
        request_headers = {
            'cookie': 'mid=YlTkmwALAAG8_hwvjoIMJQK68cpC; ig_did=7F40C175-A233-4640-BCA4-41546EB3533D; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; dpr=1.25; datr=azRyYqr5KFpgjE009pBFeTyu; shbid="478\05453094873418\0541683262590:01f7abf35b9b15790afd6da1998c0a6c04b516de37658e4c94b19682388a62e31eb9c790"; shbts="1651726590\05453094873418\0541683262590:01f73fe05d535571e3b520d284d9724ba0f892c957e7b1f733636cdd0421d553099be456"; fbsr_124024574287414=x8BX7TobCGuoo8ZLLOTF7YORu6dzdB8kc99QpUWD3kU.eyJ1c2VyX2lkIjoiMTAwMDA0MzIyNDA2NTgzIiwiY29kZSI6IkFRQXhrM21QM1UtRE8zUk9yWU1BZWF4U0FFaFUxRDhXcHU3TnVYMWZzRm9vbnYzalFSV1B1dkJtRjhVTldfOVAtZ21YSFJjTHU3dUU0Um9DTVZwWko1U2I4MzdYcEhhU3RTOXE1ckxEbXFoaG9MRzBWSmludHItaWpYVXptNEZVOHpteHlNck05SXFwVWduZDRmXzV3a0Nrcktma01hd3VpTm95ZEFIQnczOG5MS2drQU53OVZScm9ucE1pUUZicjQyVVRjal9uWnRUVG52OXUyZzU1TnZIdDYtTm45YVA1NkVSV1hyNlA4QTVjeFRuZF8ycktDeUVubWZXRjJvMFFnRk12MVBaallCZkxuWENjTDA0RlN5ZGhqTmFrWUh4RzkyTjZWN3Jxc2dwSUo3OEI0d1E2emg2S3V3cGI4bFZFbEg1UXYxNzRSTGowTjNNZkJWZjk1NzNTIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUlBMnJrZEFLV2N6aVRJWVhiOXowR1dNcWRaQ1Y3MVpCNVpDNjhLcDBaQmRaQnRpZTVmWXpoMWE4ZTh2SzFlU0FXTGhIYU1jNzRFMHpkcHM2M1ByNnJwTFRaQWI3bEFQNjFPYUVlSWM3dTBwMHNOT1ZNOWVuanVLY3BzS3ozdXhjN0VmVEJ4NlhUekVhalhMWGdUSnZVVGY5ckd5anJkRkdQVGg2OXpTc2giLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTY1MTczNzYzN30; csrftoken=h2w9VIoMkD1x35S5C7oa38RoUEYW01wa; ds_user_id=2955836353; sessionid=2955836353%3AZ4ICKx8RLE2LV9%3A27; fbsr_124024574287414=x8BX7TobCGuoo8ZLLOTF7YORu6dzdB8kc99QpUWD3kU.eyJ1c2VyX2lkIjoiMTAwMDA0MzIyNDA2NTgzIiwiY29kZSI6IkFRQXhrM21QM1UtRE8zUk9yWU1BZWF4U0FFaFUxRDhXcHU3TnVYMWZzRm9vbnYzalFSV1B1dkJtRjhVTldfOVAtZ21YSFJjTHU3dUU0Um9DTVZwWko1U2I4MzdYcEhhU3RTOXE1ckxEbXFoaG9MRzBWSmludHItaWpYVXptNEZVOHpteHlNck05SXFwVWduZDRmXzV3a0Nrcktma01hd3VpTm95ZEFIQnczOG5MS2drQU53OVZScm9ucE1pUUZicjQyVVRjal9uWnRUVG52OXUyZzU1TnZIdDYtTm45YVA1NkVSV1hyNlA4QTVjeFRuZF8ycktDeUVubWZXRjJvMFFnRk12MVBaallCZkxuWENjTDA0RlN5ZGhqTmFrWUh4RzkyTjZWN3Jxc2dwSUo3OEI0d1E2emg2S3V3cGI4bFZFbEg1UXYxNzRSTGowTjNNZkJWZjk1NzNTIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUlBMnJrZEFLV2N6aVRJWVhiOXowR1dNcWRaQ1Y3MVpCNVpDNjhLcDBaQmRaQnRpZTVmWXpoMWE4ZTh2SzFlU0FXTGhIYU1jNzRFMHpkcHM2M1ByNnJwTFRaQWI3bEFQNjFPYUVlSWM3dTBwMHNOT1ZNOWVuanVLY3BzS3ozdXhjN0VmVEJ4NlhUekVhalhMWGdUSnZVVGY5ckd5anJkRkdQVGg2OXpTc2giLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTY1MTczNzYzN30; rur="EAG\0542955836353\0541683273780:01f73d7e5918b65f996f161cfe89d74883fbd22b8deba334c47b654d04602996b01334d5"'
            } 
        response = requests.get(url,headers = request_headers)
        cnt = 0
        for i in range(3):
            for j in range(3):
              cnt += response.json()['data']['top']['sections'][i]['layout_content']['medias'][j]['media']['like_count']

        result = round(cnt/9,0)
    except:
        response = requests.get(url)
        cnt = response.json()['data']['top']['sections'][0]['layout_content']['medias'][0]['media']['like_count']
    
    
    return result