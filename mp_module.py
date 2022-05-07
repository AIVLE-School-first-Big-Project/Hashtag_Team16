import requests
from multiprocessing import Pool

def get_json_data(target):
    return
def hashtag_cnt_crawling(target):
    target = target[1:]
    url = 'https://www.instagram.com/explore/tags/'+ target +'/?__a=1&__d=dis'
    try:
        request_headers = {
            'cookie': 'mid=YlTkmwALAAG8_hwvjoIMJQK68cpC; ig_did=7F40C175-A233-4640-BCA4-41546EB3533D; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; dpr=1.25; datr=azRyYqr5KFpgjE009pBFeTyu; shbid="478\05453094873418\0541683262590:01f7abf35b9b15790afd6da1998c0a6c04b516de37658e4c94b19682388a62e31eb9c790"; shbts="1651726590\05453094873418\0541683262590:01f73fe05d535571e3b520d284d9724ba0f892c957e7b1f733636cdd0421d553099be456"; csrftoken=TbwV49OHhtDujO7Kekmsy7KgXoDasFAe; ds_user_id=53094873418; sessionid=53094873418%3AUjugqzy3M0GPLG%3A7; fbsr_124024574287414=u611PbFc6EIfFHJ5r3XsS8qV5UBqmZ3j6xzUnw3sL98.eyJ1c2VyX2lkIjoiMTAwMDA0MzIyNDA2NTgzIiwiY29kZSI6IkFRQko1UGw2SFg1eTFpLXFlekFkV3ZyV2YtaTVXUlltTjFPWjlqMS1xZHBfWXpWRUpJeklCLVppY1JLYjFqV3NXdlF4RGJkbzdoeXZpZlZqSDd5bXU0V0NtWW1jbDN3MmhrV0FmSFZrRWhlbE1LT3JRd3VoT01EVkQ2QlQ0VHJkTWpJYVQ0dXBmSUcwY3NJLWF1dElxc3QzcEVzOHg0RW5iOFZZVHVEUHp3V0pLbm9FeEt4eWJVamw3YjhYQTZmX2tfQnIwcm1hb1l5Sk9nNkdnSEFTYlp4aV9XUnJIS05SN0FaR0dENmFzZUEtM1Azdm4yMlU0T0dLbHlUaTVBZ1Z3VWJLb0p3Z3BwRDNjQ0Rtb2RXbkV4cG1VdXRISXpRV3Z6WVlRTGJBYWRLZl84MDZFUlVETkhzd0VFd0oteHNVZTNFeWs3R1pLbjBXMWxiLTU5SjFWRmY3Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUl4MWpEWkJOMzVaQTNGWE52YzdBcVE5OE5KTVZhN0hXM3NHcHJyemhEYWpIbUlaQ1Q4emJtNmNPbm1UVDNUV0IxaHROa0hldUNqWkE2S3dZWkFXWWcyMW82MUZhSkIyMUtFZ1RldEpQQ0Y3TDc3WkJMTVRRQ3Zqc0hqQWQwdDA5RXhkZEFiYTNSZ2RRMVhYNVNtWkNDWkFJajQ4MFRsdlgweG9Ca0ZGQmt0WkEiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTY1MTkwNjgwNH0; rur="NAO\05453094873418\0541683442889:01f78ca4168e0663c4e66b9090775808307dad4ba5e14681198d314517589e522b894c57"'}
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
            'cookie': 'mid=YlTkmwALAAG8_hwvjoIMJQK68cpC; ig_did=7F40C175-A233-4640-BCA4-41546EB3533D; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; dpr=1.25; datr=azRyYqr5KFpgjE009pBFeTyu; shbid="478\05453094873418\0541683262590:01f7abf35b9b15790afd6da1998c0a6c04b516de37658e4c94b19682388a62e31eb9c790"; shbts="1651726590\05453094873418\0541683262590:01f73fe05d535571e3b520d284d9724ba0f892c957e7b1f733636cdd0421d553099be456"; csrftoken=TbwV49OHhtDujO7Kekmsy7KgXoDasFAe; ds_user_id=53094873418; sessionid=53094873418%3AUjugqzy3M0GPLG%3A7; fbsr_124024574287414=u611PbFc6EIfFHJ5r3XsS8qV5UBqmZ3j6xzUnw3sL98.eyJ1c2VyX2lkIjoiMTAwMDA0MzIyNDA2NTgzIiwiY29kZSI6IkFRQko1UGw2SFg1eTFpLXFlekFkV3ZyV2YtaTVXUlltTjFPWjlqMS1xZHBfWXpWRUpJeklCLVppY1JLYjFqV3NXdlF4RGJkbzdoeXZpZlZqSDd5bXU0V0NtWW1jbDN3MmhrV0FmSFZrRWhlbE1LT3JRd3VoT01EVkQ2QlQ0VHJkTWpJYVQ0dXBmSUcwY3NJLWF1dElxc3QzcEVzOHg0RW5iOFZZVHVEUHp3V0pLbm9FeEt4eWJVamw3YjhYQTZmX2tfQnIwcm1hb1l5Sk9nNkdnSEFTYlp4aV9XUnJIS05SN0FaR0dENmFzZUEtM1Azdm4yMlU0T0dLbHlUaTVBZ1Z3VWJLb0p3Z3BwRDNjQ0Rtb2RXbkV4cG1VdXRISXpRV3Z6WVlRTGJBYWRLZl84MDZFUlVETkhzd0VFd0oteHNVZTNFeWs3R1pLbjBXMWxiLTU5SjFWRmY3Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUl4MWpEWkJOMzVaQTNGWE52YzdBcVE5OE5KTVZhN0hXM3NHcHJyemhEYWpIbUlaQ1Q4emJtNmNPbm1UVDNUV0IxaHROa0hldUNqWkE2S3dZWkFXWWcyMW82MUZhSkIyMUtFZ1RldEpQQ0Y3TDc3WkJMTVRRQ3Zqc0hqQWQwdDA5RXhkZEFiYTNSZ2RRMVhYNVNtWkNDWkFJajQ4MFRsdlgweG9Ca0ZGQmt0WkEiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTY1MTkwNjgwNH0; rur="NAO\05453094873418\0541683442889:01f78ca4168e0663c4e66b9090775808307dad4ba5e14681198d314517589e522b894c57"'
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
            'cookie': 'mid=YlTkmwALAAG8_hwvjoIMJQK68cpC; ig_did=7F40C175-A233-4640-BCA4-41546EB3533D; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; dpr=1.25; datr=azRyYqr5KFpgjE009pBFeTyu; shbid="478\05453094873418\0541683262590:01f7abf35b9b15790afd6da1998c0a6c04b516de37658e4c94b19682388a62e31eb9c790"; shbts="1651726590\05453094873418\0541683262590:01f73fe05d535571e3b520d284d9724ba0f892c957e7b1f733636cdd0421d553099be456"; csrftoken=TbwV49OHhtDujO7Kekmsy7KgXoDasFAe; ds_user_id=53094873418; sessionid=53094873418%3AUjugqzy3M0GPLG%3A7; fbsr_124024574287414=u611PbFc6EIfFHJ5r3XsS8qV5UBqmZ3j6xzUnw3sL98.eyJ1c2VyX2lkIjoiMTAwMDA0MzIyNDA2NTgzIiwiY29kZSI6IkFRQko1UGw2SFg1eTFpLXFlekFkV3ZyV2YtaTVXUlltTjFPWjlqMS1xZHBfWXpWRUpJeklCLVppY1JLYjFqV3NXdlF4RGJkbzdoeXZpZlZqSDd5bXU0V0NtWW1jbDN3MmhrV0FmSFZrRWhlbE1LT3JRd3VoT01EVkQ2QlQ0VHJkTWpJYVQ0dXBmSUcwY3NJLWF1dElxc3QzcEVzOHg0RW5iOFZZVHVEUHp3V0pLbm9FeEt4eWJVamw3YjhYQTZmX2tfQnIwcm1hb1l5Sk9nNkdnSEFTYlp4aV9XUnJIS05SN0FaR0dENmFzZUEtM1Azdm4yMlU0T0dLbHlUaTVBZ1Z3VWJLb0p3Z3BwRDNjQ0Rtb2RXbkV4cG1VdXRISXpRV3Z6WVlRTGJBYWRLZl84MDZFUlVETkhzd0VFd0oteHNVZTNFeWs3R1pLbjBXMWxiLTU5SjFWRmY3Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUl4MWpEWkJOMzVaQTNGWE52YzdBcVE5OE5KTVZhN0hXM3NHcHJyemhEYWpIbUlaQ1Q4emJtNmNPbm1UVDNUV0IxaHROa0hldUNqWkE2S3dZWkFXWWcyMW82MUZhSkIyMUtFZ1RldEpQQ0Y3TDc3WkJMTVRRQ3Zqc0hqQWQwdDA5RXhkZEFiYTNSZ2RRMVhYNVNtWkNDWkFJajQ4MFRsdlgweG9Ca0ZGQmt0WkEiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTY1MTkwNjgwNH0; rur="NAO\05453094873418\0541683442889:01f78ca4168e0663c4e66b9090775808307dad4ba5e14681198d314517589e522b894c57"'}
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
        result = {a : b for a,b in temp_result}
        return result