import requests
from multiprocessing import Pool

def hashtag_cnt_crawling(target):
    target = target[1:]
    url = 'https://www.instagram.com/explore/tags/'+ target +'/?__a=1&__d=dis'
    try:
        request_headers = {
            'cookie' : 'mid=YnTOIQALAAG2A1_J5CA6wXHBlU0b; ig_did=D8D0A136-EB77-4B78-80BB-164EE20D1E38; ig_nrcb=1; csrftoken=Z6d0MFGUexGIMX5SYhwUTcj2ozFsNLkL; ds_user_id=53290782834; sessionid=53290782834:2LtP5O1dtffItA:29; rur="VLL\05453290782834\0541683444288:01f7473a9b07ed196f32adfa02a3719eb04022d1563044e26a58512fb45577fc9a2526bd"'
            }
            
        response = requests.get(url ,headers = request_headers)
        cnt = response.json()['data']['media_count']
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
    with Pool(8) as p:
        temp_result = p.map(hashtag_cnt_crawling, x)
        return {a : b for a,b in temp_result}