from django.shortcuts import render,redirect
from django.http import HttpResponse
from qna.models import *
import joblib
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS, ALSModel

def index(request):
    global neural_network,als_model,pics,recommender_df,hashtags_df
    #######모델 불러오기 (dnn feature뽑아오기,als 해시태그 추천)
    model_path='C:/django/Hashtag_Team16/modeling/mobilenetv2.pkl'
    neural_network = joblib.load(model_path)
    spark = SparkSession.builder.master('local').appName('all').getOrCreate()
    als_model = ALSModel.load('C:/django/Hashtag_Team16/modeling/als')

    #######데이터 불러오기 (pics 이미지의 피처 데이터프레임,hashtags_df 모든해시태그, recommender_df 추천df)
    pics=joblib.load('C:/django/Hashtag_Team16/modeling/pics_0424_1-001.pkl')
    recommender_df=joblib.load('C:/django/Hashtag_Team16/modeling/recommender_df_0424_1.pkl')
    hashtags_df=joblib.load('C:/django/Hashtag_Team16/modeling/hashtags_df_0424_1.pkl')
    # Login이 안된 상태에서는 연결하지 못하도록         
    try:
        user = USER.objects.get(user_id=request.session['user_id']).user_id
        request.session['user_id']
        return render(request, 'main/index.html', {'user' : user})
    except KeyError:
        return redirect('/')

def function(request):
    try:
        user = USER.objects.get(user_id=request.session['user_id']).user_id                
        request.session['user_id']
        return render(request, 'main/function.html', {'user' : user})
    except KeyError:
        return redirect('/')
