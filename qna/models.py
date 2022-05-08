# Create your models here.
from django.db import models
# Create your models here.
class USER(models.Model):
    
    
    user_id = models.CharField(primary_key=True,  max_length=20, null=False)
    pw = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=20, null=False)
    birth_year = models.IntegerField(null=False)
    birth_month = models.IntegerField(null=False)
    birth_day = models.IntegerField(null=False)
    email = models.CharField(max_length=50, null=True)
    phone_num = models.CharField(max_length=20, null=True)
    usage_count = models.IntegerField(null=True)
    join_date = models.DateTimeField(null=True)
    account_state = models.CharField(max_length=30 , null=True)
    login_date = models.DateTimeField(null=True)

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
    board = models.ForeignKey(BOARD,  db_column='board_id', on_delete=models.CASCADE, null=False)
    #a_user_id = models.CharField(max_length=20,null=False)
    user = models.ForeignKey(USER, db_column='a_user_id', on_delete=models.CASCADE, null=False)

    title = models.CharField(max_length=50,null=False)
    content = models.TextField(null=False)
    date = models.DateTimeField(null=True, auto_now=True)
    #image = models.ImageField(upload_to='db_image/image_folder/')
    image = models.CharField(max_length=300, null=False)
    comment_cnt = models.IntegerField(null=True)


    class Meta:
        db_table = 'article'
        managed = False

class COMMENT(models.Model):

    comment_id = models.AutoField(primary_key=True, null=False)
    #c_user_id = models.CharField(max_length=20,null=False)
    user = models.ForeignKey(USER, db_column='c_user_id', on_delete=models.CASCADE, null=False)    
    content = models.CharField(max_length=50, null=False)
    date = models.DateTimeField(null=True, auto_now=True)
    #article_id = models.IntegerField(null=False)
    article = models.ForeignKey(ARTICLE,  db_column='article_id', on_delete=models.CASCADE, null=False)
    
    class Meta:
        db_table = 'comment'
        managed = False


class LOG(models.Model):
    log_id = models.AutoField(primary_key=True, null=False)
    #l_user_id = models.CharField(max_length=20,null=False)
    user = models.ForeignKey(USER, db_column='l_user_id', on_delete=models.CASCADE, null=False)

    service_score = models.IntegerField(null=False)
    feedback = models.TextField(null=True)
    #image = models.FileField(upload_to='%Y/%m/%d',null=True)
    #image = models.ImageField(upload_to='db_image/image_folder/')
    image = models.CharField(max_length=300, null=False)
    prior_tag = models.TextField(null=False)
    #after_tag = models.TextField(null=False)
    result1 = models.CharField(max_length=300, null=False)
    result2 = models.CharField(max_length=300, null=False)
    result3 = models.CharField(max_length=300, null=False)
    result4 = models.CharField(max_length=300, null=False)

    
    class Meta:
        db_table = 'log'
        managed = False