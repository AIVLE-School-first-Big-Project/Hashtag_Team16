import requests
from multiprocessing import Pool


def hashtag_cnt_crawling(target):
    target = target[1:]
    url = 'https://www.instagram.com/explore/tags/'+ target +'/?__a=1&__d=dis'
    try:
        request_headers = {
            'cookie' : 'mid=YneXhAALAAFOLyC612t4We-ckroZ; ig_did=DF0D006A-7C5F-4B47-BF68-AF3425D9B17B; ig_nrcb=1; csrftoken=wz0XSb7jK9ho69CeEjnNvrLMgYwBQu5R; ds_user_id=49450739206; sessionid=49450739206%3AkAkXHcRx23bKzM%3A23; rur="PRN\05449450739206\0541683598854:01f7a4f3fbf697ab6e08d758d7036b11082c6c10d15b6ecfee3b436543042b046229c6f2"'
        }
        response = requests.get(url ,headers = request_headers)
        cnt = response.json()
        return (target, cnt)
    except KeyError:
        response = requests.get(url)
        cnt = response.json()['graphql']['hashtag']['edge_hashtag_to_media']['count']
        return (target, cnt)
    
def hashtag_influ_crawling(target):
    url = 'https://www.instagram.com/explore/tags/'+ target +'/?__a=1&__d=dis'
    
    try:
        request_headers = {
            'cookie' : 'mid=YnTOIQALAAG2A1_J5CA6wXHBlU0b; ig_did=D8D0A136-EB77-4B78-80BB-164EE20D1E38; ig_nrcb=1; csrftoken=Z6d0MFGUexGIMX5SYhwUTcj2ozFsNLkL; ds_user_id=53290782834; sessionid=53290782834:2LtP5O1dtffItA:29; rur="VLL\05453290782834\0541683444288:01f7473a9b07ed196f32adfa02a3719eb04022d1563044e26a58512fb45577fc9a2526bd"'
        }
        response = requests.get(url,headers = request_headers)
        cnt = response.json()['data']['top']['sections'][0]['layout_content']['medias'][0]['media']['user']['username']
    except KeyError:
        response = requests.get(url)
        cnt = response.json()['graphql']['hashtag']['edge_hashtag_to_media']['count']
        
    return cnt

def hashtag_likes_crawling(target):
    # import requests
    url = 'https://www.instagram.com/explore/tags/'+ target +'/?__a=1&__d=dis'
    try:
        request_headers = {
            'cookie' : 'mid=YnTOIQALAAG2A1_J5CA6wXHBlU0b; ig_did=D8D0A136-EB77-4B78-80BB-164EE20D1E38; ig_nrcb=1; csrftoken=Z6d0MFGUexGIMX5SYhwUTcj2ozFsNLkL; ds_user_id=53290782834; sessionid=53290782834:2LtP5O1dtffItA:29; rur="VLL\05453290782834\0541683444288:01f7473a9b07ed196f32adfa02a3719eb04022d1563044e26a58512fb45577fc9a2526bd"'
        }
        response = requests.get(url,headers = request_headers)
        cnt = 0
        for i in range(3):
            for j in range(3):
                cnt += response.json()['data']['top']['sections'][i]['layout_content']['medias'][j]['media']['like_count']

        result = round(cnt/9,0)
    except KeyError:
        response = requests.get(url)
        cnt = response.json()['data']['top']['sections'][0]['layout_content']['medias'][0]['media']['like_count']
    
    
    return result



def mult_process_tag(x):
    with Pool(6) as p:
        temp_result = p.map(hashtag_cnt_crawling, x)
        result = {a : b['data']['media_count'] for a,b in temp_result}
        influ = temp_result[0][1]['data']['top']['sections'][0]['layout_content']['medias'][0]['media']['user']['username']
        likes= 0
        for i in range(3):
            for j in range(3):
                likes += temp_result[0][1]['data']['top']['sections'][i]['layout_content']['medias'][j]['media']['like_count']
        avg_like = round(likes/9,0)
    return result, influ, avg_like