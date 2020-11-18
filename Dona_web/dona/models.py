from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.utils import timezone
from datetime import datetime
from django.conf import settings

class User(AbstractUser):
    Nickname=models.CharField(max_length=10)
    coin=models.IntegerField(default=10)
    region1=models.CharField(max_length=50,null=True)
    region2=models.CharField(max_length=50,null=True)

class region(models.Model):
    objects = models.Manager()
    region_id=models.IntegerField()
    region_name = models.CharField(max_length=50, blank=True)

class help_board(models.Model):
    objects = models.Manager()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='작성자')
    title=models.CharField(max_length=50)
    content = models.TextField(verbose_name='내용')
    region=models.CharField(max_length=50, verbose_name='도움 지역')
    region_last=models.CharField(max_length=20,verbose_name='도움 지역 읍면동', null=True)
    help_coin=models.IntegerField(verbose_name='코인 개수',default=10)
    hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    help_date = models.DateTimeField(verbose_name='도움 요청일',default=datetime.now, blank=True)
    top_fixed = models.BooleanField(verbose_name='상단고정', default=False)
    finished = models.BooleanField(verbose_name='마감 여부', default=False)
    
    def __str__(self):
        return self.title
