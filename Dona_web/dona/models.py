from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    Nickname=models.CharField(max_length=10)
    coin=models.IntegerField(default=10)
    region1=models.CharField(max_length=50,null=True)
    region2=models.CharField(max_length=50,null=True)

class region(models.Model):
    objects = models.Manager()
    region_id=models.IntegerField()
    region_name = models.CharField(max_length=50, blank=True)