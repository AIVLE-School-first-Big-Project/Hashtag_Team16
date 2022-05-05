import requests
from multiprocessing import Pool

def hashtag_cnt_crawling(target):
    target = target[1:]
    url = 'https://www.instagram.com/explore/tags/'+ target +'/?__a=1&__d=dis'
    try:
        request_headers = {
            'cookie' : 'ig_did=9218D585-1D45-43F2-8CD8-551A16853932; ig_nrcb=1; mid=YmwBYAALAAH-JdcTDWyYG3JrAfjD; fbm_124024574287414=base_domain=.instagram.com; datr=BF5tYmZtnVsJotuwxMLxEXCS; shbid="11862\0541994601200\0541683075730:01f73c42489b8d6f5ee1f821a6aad3eeb95f5cf1b997832aa7aefcb86c45ef5885a25d9f"; shbts="1651539730\0541994601200\0541683075730:01f72f006f5f41b9af5b62a6d9f36cdb6b0c4cc89564cd99752f25f70597f1ed97fffce7"; csrftoken=lF08QydrVyuCWNssIa4HCJ5gRpSGsiF6; ds_user_id=1994601200; sessionid=1994601200%3AbHVDMgen5K46Ph%3A29; fbsr_124024574287414=zM2yABgZqpJGemiq8pJzm7b9oOH7J-CQIi0mucWPaIE.eyJ1c2VyX2lkIjoiMTAwMDAzMjU2MDc3NDUzIiwiY29kZSI6IkFRRFNlTkhaXzh2MEZUN01CQ040OENqTVdBc1ZpZHBCcm1mMWlDY0JWa0l0NmRkaWpES2dvWGRSMEkyZmtLT200dTlKclhCOExGUDUtSGRvS1pZb2VoMmo5eUZScWlBWjdRTGZhd1NMWFJCRXdacjUzeWFGWjdzTFdsRGIwajZwc1JsTTB3TGYtaXdNaXhGTmMtVHlseEJJZFBUN2FDZUhyMkIyWGcxMzRhR1hOZ2NoS1pmWXR2ZGU2bVZadEZ2MmhHaEgzSzNSN2pLeW5oYWdZWVk4MVpVSWlaRnhPWFR5N1VUb2l4ZW9DUTk0UHF3NzlXVms1QVNxWXVlTjFoY0E5QkpMWDN2TGFBVE1kYTlfMWdWTFNmTWYzY1lFc051Zl9VOGVZZmNLNlAtQi0wekkxdllLZ2hna2pwZDJqNV84VWZpeXlnd3N3NUtIcFlMcEFqTWNtOGMtIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQU5xenM4VXZoemwzWkFZWkJiTkc1ZnFrMzluRDY3b2tYZUlXY3NaQ29vVDBnMnZ6UG1aQWQzd2tDYXg2ZFlZWkNNUk51R3hsT21NQ3Fsd1dKUGVUNjQzRUZuVjBrN2E4a3RTclBnblpDOWFLeG9tV3djZ1pDZ3VaQmNQZTlTN0psSTg3Q0VuT1pCdmpIVkRpdXBSUU1QTVBqUUNkWkNWNERGSkdLS0hJQkNVNlhLRVhEbzRuWkE2T3BvWkQiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTY1MTc1Mzg3OX0; fbsr_124024574287414=zM2yABgZqpJGemiq8pJzm7b9oOH7J-CQIi0mucWPaIE.eyJ1c2VyX2lkIjoiMTAwMDAzMjU2MDc3NDUzIiwiY29kZSI6IkFRRFNlTkhaXzh2MEZUN01CQ040OENqTVdBc1ZpZHBCcm1mMWlDY0JWa0l0NmRkaWpES2dvWGRSMEkyZmtLT200dTlKclhCOExGUDUtSGRvS1pZb2VoMmo5eUZScWlBWjdRTGZhd1NMWFJCRXdacjUzeWFGWjdzTFdsRGIwajZwc1JsTTB3TGYtaXdNaXhGTmMtVHlseEJJZFBUN2FDZUhyMkIyWGcxMzRhR1hOZ2NoS1pmWXR2ZGU2bVZadEZ2MmhHaEgzSzNSN2pLeW5oYWdZWVk4MVpVSWlaRnhPWFR5N1VUb2l4ZW9DUTk0UHF3NzlXVms1QVNxWXVlTjFoY0E5QkpMWDN2TGFBVE1kYTlfMWdWTFNmTWYzY1lFc051Zl9VOGVZZmNLNlAtQi0wekkxdllLZ2hna2pwZDJqNV84VWZpeXlnd3N3NUtIcFlMcEFqTWNtOGMtIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQU5xenM4VXZoemwzWkFZWkJiTkc1ZnFrMzluRDY3b2tYZUlXY3NaQ29vVDBnMnZ6UG1aQWQzd2tDYXg2ZFlZWkNNUk51R3hsT21NQ3Fsd1dKUGVUNjQzRUZuVjBrN2E4a3RTclBnblpDOWFLeG9tV3djZ1pDZ3VaQmNQZTlTN0psSTg3Q0VuT1pCdmpIVkRpdXBSUU1QTVBqUUNkWkNWNERGSkdLS0hJQkNVNlhLRVhEbzRuWkE2T3BvWkQiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTY1MTc1Mzg3OX0; rur="VLL\0541994601200\0541683290207:01f7d5f494c3681837f53e2ce770da1ddc4052da5591a08544c22d1c800ce817171670b4"'
        }
        response = requests.get(url ,headers = request_headers)
        cnt = response.json()['data']['media_count']
        return (target, cnt)
    except:
        
        response = requests.get(url)
        cnt = response.json()['graphql']['hashtag']['edge_hashtag_to_media']['count']
        return (target, cnt)
    
def mult_process(x):
    with Pool(8) as p:
        temp_result = p.map(hashtag_cnt_crawling, x)
        return {a : b for a,b in temp_result}