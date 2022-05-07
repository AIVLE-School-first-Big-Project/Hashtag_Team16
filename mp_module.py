import requests
from multiprocessing import Pool

def hashtag_cnt_crawling(target):
    target = target[1:]
    url = 'https://www.instagram.com/explore/tags/'+ target +'/?__a=1&__d=dis'
    try:
        request_headers = {
            'cookie' : 'mid=YnTOCAALAAHUbix67X3875H_OG2G; ig_did=ABD3C269-43E1-45CF-B7C2-B0862B36F6C8; ig_nrcb=1; shbid="11862\0541994601200\0541683358097:01f713ea00eaefb1edf0f9bfb63983d4f2c01021000717296b4e602a480f45d58fc330a8"; shbts="1651822097\0541994601200\0541683358097:01f7bef1422b6281d9c5b2f8a9698306b31b4b16942fb7a602c3066497e4f40ea7b06861"; csrftoken=Qn2L4u1CUfC5QPnsNsO6jWqsdF2Ua6bc; ds_user_id=52748895430; sessionid=52748895430%3AmkUAtrlswAh1iJ%3A26; rur="PRN\05452748895430\0541683358577:01f7e03590bd1b590f4f74c953477df02fea67602eb5172240c36f502f5569d398c4e67f"'}
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
            'cookie': 'mid=YnTOCAALAAHUbix67X3875H_OG2G; ig_did=ABD3C269-43E1-45CF-B7C2-B0862B36F6C8; ig_nrcb=1; shbid="11862\0541994601200\0541683358097:01f713ea00eaefb1edf0f9bfb63983d4f2c01021000717296b4e602a480f45d58fc330a8"; shbts="1651822097\0541994601200\0541683358097:01f7bef1422b6281d9c5b2f8a9698306b31b4b16942fb7a602c3066497e4f40ea7b06861"; csrftoken=Qn2L4u1CUfC5QPnsNsO6jWqsdF2Ua6bc; ds_user_id=52748895430; sessionid=52748895430%3AmkUAtrlswAh1iJ%3A26; rur="PRN\05452748895430\0541683358577:01f7e03590bd1b590f4f74c953477df02fea67602eb5172240c36f502f5569d398c4e67f"'
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
            'cookie' : 'mid=YnTOCAALAAHUbix67X3875H_OG2G; ig_did=ABD3C269-43E1-45CF-B7C2-B0862B36F6C8; ig_nrcb=1; shbid="11862\0541994601200\0541683358097:01f713ea00eaefb1edf0f9bfb63983d4f2c01021000717296b4e602a480f45d58fc330a8"; shbts="1651822097\0541994601200\0541683358097:01f7bef1422b6281d9c5b2f8a9698306b31b4b16942fb7a602c3066497e4f40ea7b06861"; csrftoken=Qn2L4u1CUfC5QPnsNsO6jWqsdF2Ua6bc; ds_user_id=52748895430; sessionid=52748895430%3AmkUAtrlswAh1iJ%3A26; rur="PRN\05452748895430\0541683358577:01f7e03590bd1b590f4f74c953477df02fea67602eb5172240c36f502f5569d398c4e67f"'}
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