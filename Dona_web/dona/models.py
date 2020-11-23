from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.utils import timezone
from datetime import datetime
from django.conf import settings

class User(AbstractUser):
    Nickname=models.CharField(max_length=6,null=True)
    helped=models.IntegerField(default=0)
    helping=models.IntegerField(default=0)
    region1=models.CharField(max_length=50,null=True)
    region2=models.CharField(max_length=50,null=True)

class region(models.Model):
    objects = models.Manager()
    region_id=models.IntegerField()
    region_name = models.CharField(max_length=50, blank=True)
    region_help=models.IntegerField(default=0)

class help_board(models.Model):
    objects = models.Manager()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='작성자')
    title=models.CharField(max_length=50)
    content = models.TextField(verbose_name='내용')
    region=models.CharField(max_length=50, verbose_name='도움 지역')
    region_last=models.CharField(max_length=20,verbose_name='도움 지역 읍면동', null=True)
    hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    help_date = models.DateTimeField(verbose_name='Dona 요청일',default=datetime.now, blank=True)
    top_fixed = models.BooleanField(verbose_name='상단고정', default=False)
    finished = models.BooleanField(verbose_name='마감 여부', default=False)
    
    def __str__(self):
        return self.title
    @property
    def update_counter(self):
        self.hits=self.hits+1
        self.save()

class messages_Container(models.Model):
    objects = models.Manager()
    title=models.CharField(max_length=50)
    userone = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user1', null=True, on_delete=models.CASCADE, verbose_name='도움 받을 사람')
    usertwo = models.ForeignKey(settings.AUTH_USER_MODEL,  related_name='user2', null=True, on_delete=models.CASCADE, verbose_name='도와줄 사람')
    unread_count = models.IntegerField(verbose_name='미확인 쪽지 수', default=0)
    message_region = models.CharField(max_length=50,blank=True)
    def __str__(self):
        return self.title

class messages(models.Model):
    objects = models.Manager()
    message = models.ForeignKey(messages_Container, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='쪽지',max_length=200)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    user_send = models.BooleanField(verbose_name='보낸이', default=True)
    didread = models.BooleanField(verbose_name='확인 여부', default=True)
    def __str__(self):
        return self.content

class Comment(models.Model):
    post=models.ForeignKey(help_board, related_name='comments', on_delete=models.CASCADE)
    author= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_text=models.TextField()
    created_at=models.DateTimeField(default=timezone.now) 

    def approve(self):
        self.save()

    def __str__(self):
        return self.comment_text
    