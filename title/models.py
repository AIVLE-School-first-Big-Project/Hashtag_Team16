from django.db import models
from django.db.models.fields import CharField, IntegerField, FloatField, DateField
from pandas import to_datetime

# Create your models here.

class USER(models.Model):

    user_id = models.CharField(primary_key=True,  max_length=20, null=False)
    pw = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=20, null=False)
    birth_year = models.IntegerField(null=False)
    birth_year = models.IntegerField(null=False)
    birth_year = models.IntegerField(null=False)
    email = models.CharField(max_length=50, null=True)
    phone_num = models.CharField(max_length=20, null=True)
    usage_count = models.IntegerField(null=False)

    class Meta:
        db_table = 'user'
        managed = False

class BOARD(models.Model):
    board_id = models.IntegerField(primary_key=True, null=False)
    board_name = models.CharField(max_length=30,null=False)
    
    class Meta:
        db_table = 'board'
        managed = False


class ARTICLE(models.Model):
    article_id = models.AutoField(primary_key = True, null=False)
    #board_id = models.IntegerField(null=False)
    #a_user_id = models.CharField(max_length=20,null=False)
    title = models.CharField(max_length=50,null=False)
    content = models.TextField(null=False)
    date = models.DateField(null=False, default=to_datetime)
    image = models.FileField(upload_to='%Y/%m/%d',null=True)

    a_user_id = models.ForeignKey(USER, db_column='user_id', on_delete=models.CASCADE, null=False)
    board_id = models.ForeignKey(BOARD,  db_column='board_id', on_delete=models.CASCADE, null=False)
    class Meta:
        db_table = 'article'
        managed = False

class COMMENT(models.Model):

    comment_id = models.AutoField(primary_key=True, null=False)
    #c_user_id = models.CharField(max_length=20,null=False)
    content = models.CharField(max_length=50, null=False)
    date = models.DateField(null=False, default=to_datetime)
    #article_id = models.IntegerField(null=False)
    
    c_user_id = models.ForeignKey(USER, db_column='user_id', on_delete=models.CASCADE, null=False)
    article_id = models.ForeignKey(ARTICLE,  db_column='article_id', on_delete=models.CASCADE, null=False)
    
    class Meta:
        db_table = 'comment'
        managed = False


class LOG(models.Model):
    log_id = models.AutoField(primary_key=True, null=False)
    #l_user_id = models.CharField(max_length=20,null=False)
    service_score = models.IntegerField(null=False)
    feedback = models.TextField(null=True)
    image = models.FileField(upload_to='%Y/%m/%d',null=True)
    prior_tag = models.TextField(null=False)
    after_tag = models.TextField(null=False)

    l_user_id = models.ForeignKey(USER, db_column='user_id', on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'log'
        managed = False