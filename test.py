import requests

def hashtag_cnt_crawling(target):
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
    
from multiprocessing import Pool


if __name__ == '__main__':
    with Pool(3) as p:
        print(p.map(hashtag_cnt_crawling, ['강아지', '멍멍이', '치와와', '멍스타그램', '개', '댕댕이', '댕스타그램']))