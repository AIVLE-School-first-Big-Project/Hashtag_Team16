import pandas as pd
import numpy as np
import joblib
import os
from glob import glob

def load_all_df(keyword, ROOT_PATH='./'):
    KEYWORD_DF_PATH = f'{ROOT_PATH}data/{keyword}'
    file_path__LS = glob(KEYWORD_DF_PATH + '/*.pkl')

    output__LS = []
    for file_path in file_path__LS:
        temp__DF = joblib.load(f'{file_path}')
        output__LS.append(temp__DF)

    return output__LS


def concat_df(df__LS):
    output_df = pd.concat(df__LS, axis=0, copy=True)
    output_df.reset_index(drop=True, inplace=True)
    return output_df



def concat_total_df(keywords, ROOT_PATH='./'):
    total_df__LS = []
    for keyword in keywords:
        keyword_df__LS = load_all_df(keyword, ROOT_PATH)
        keyword_df = concat_df(keyword_df__LS)
        total_df__LS.append(keyword_df)
        
    total_df = concat_df(total_df__LS)
    return total_df





def null_processing(df, thresh=0):
    """좋아요가 thresh이상인 것만 가져옴. 기본값은 좋아요 상관없이 다 가져옴."""
    output_df = df.dropna().copy() #해시태그 null값, 게시글url, 이미지url 제거
    output_df = output_df.loc[(output_df['이미지파일명'] != 'NaN') & (output_df['좋아요'] >= thresh)].copy()
    output_df = output_df.loc[(output_df['검색키워드'] != 'NaN') | (output_df['파일경로'] != 'NaN') | 
                              (output_df['게시글url'] != 'NaN') | (output_df['이미지url'] != 'NaN')].copy()
    output_df.reset_index(drop=True, inplace=True)
    return output_df



# # 해시태그 필터링(전부, 검색키워드(카테고리)별로)

# ## 리스트에서 원소에 문자열 들어가는지확인

# In[9]:


def filtering_in_list_IN(input_list, ban):
    list2SRS = pd.Series(input_list)
    TF_SRS = list2SRS.apply(lambda x : ban not in x)
    
    #금지어가 들어가지 않은 것들만 재할당.
    list2SRS = list2SRS.loc[TF_SRS]
    output_list = list(list2SRS)
    return output_list


# In[10]:


def filtering_in_list_OUT(input_list, ban_list):
    """ 데이터프레임 셀 하나에 대해서 실행하는 함수임. """
    # 각각의 금지어를 전부 적용.
    for ban in ban_list:
        input_list = filtering_in_list_IN(input_list, ban)
        
    return input_list



def filtering_in_all(df, ban_list=[]):
    df['해시태그'] = df['해시태그'].apply(lambda x : filtering_in_list_OUT(x, ban_list))
    return df



def filtering_in_category(df, ban_list=[], category=''):
    cate_df = df.loc[df['검색키워드'] == category].copy()
    outer_df = df.loc[df['검색키워드'] != category].copy()
    
    cate_df['해시태그'] = cate_df['해시태그'].apply(lambda x : filtering_in_list_OUT(x, ban_list))
    output_df = pd.concat([cate_df, outer_df],axis=0, copy=True)
    output_df.reset_index(drop=True, inplace=True)
    return output_df



def drop_same_image1(df):
    url_counts__SRS = df['게시글url'].value_counts()
    same_url__SRS = url_counts__SRS[url_counts__SRS > 1]
    tf__SRS = df['게시글url'].isin(same_url__SRS.index)
    output_df = df[~tf__SRS].copy()
    output_df.reset_index(drop=True, inplace=True)
    return output_df



def drop_same_image2(df):
    url_counts__SRS = df['이미지url'].value_counts()
    same_url__SRS = url_counts__SRS[url_counts__SRS > 1]
    tf__SRS = df['이미지url'].isin(same_url__SRS.index)
    output_df = df[~tf__SRS].copy()
    output_df.reset_index(drop=True, inplace=True)
    return output_df



def drop_same_image3(df):
    i = 0
    while True:
        df.reset_index(drop=True, inplace=True)
        first_list = df['해시태그'].iloc[i]
        first_index = df.iloc[i:i+1].index
        in_df = df.iloc[i+1:].copy()
    
        same_idx__LS = []
        for ii in range(len(in_df)):
            second_list = in_df['해시태그'].iloc[ii]
            second_index = in_df.iloc[ii:ii+1].index

            if set(first_list) == set(second_list):
                same_idx__LS.append(second_index)
            else:
                pass
            
        df.drop(index=same_idx__LS, inplace=True)
        if len(df) == i+1:
            break

        i += 1
    df.reset_index(drop=True, inplace=True)
    return df

################## 여기서부터 사용 ###########################

def total_proprecessing(keywords, ROOT_PATH='./', thresh=0):
    """ 키워드(list)와 경로를 넣으면, 해당 키워드 폴더로 저장된 데이터프레임을 전부 다 가져옴"""
    df = concat_total_df(keywords, ROOT_PATH)
    df = null_processing(df, thresh)
    return df



def filtering_in_all(df, ban_list=[]):
    """없애고 싶은 단어를 집어넣으면, 데이터프레임 전체에 해당 단어가 포함된 해시태그를 삭제한다."""
    df['해시태그'] = df['해시태그'].apply(lambda x : filtering_in_list_OUT(x, ban_list))
    return df


def filtering_in_category(df, ban_list=[], category=''):
    """원하는 검색 키워드만을 선택해서, 없애고 싶은 단어가 포함된 해시태그를 제거한다."""
    cate_df = df.loc[df['검색키워드'] == category].copy()
    outer_df = df.loc[df['검색키워드'] != category].copy()
    
    cate_df['해시태그'] = cate_df['해시태그'].apply(lambda x : filtering_in_list_OUT(x, ban_list))
    output_df = pd.concat([cate_df, outer_df],axis=0, copy=True)
    output_df.reset_index(drop=True, inplace=True)
    return output_df



def drop_same_image(df):
    """데이터프레임 전처리(게시글url과 이미지url이 겹치는 것들을 하나만 남기고 삭제한다)"""
    df = df.drop_duplicates(['게시글url'], keep='first')
    df = df.drop_duplicates(['이미지url'], keep='first')
    #df = df.drop_same_image3(['해시태그'], keep='first') 미완
    return df

