from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.query_utils import subclasses
from .manager import UserManager
from video.models import *


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=14)
    is_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100 , null=True , blank=True)
    forget_password_token = models.CharField(max_length=100, null=True , blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)


    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    

class SubscriptionHistory(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100 , null=True , blank=True)
    razor_payment_id = models.CharField(max_length=100 , null=True , blank=True)    
    is_payment_successful = models.BooleanField(default=False)
    subscription = models.ForeignKey(SubscriptionType , on_delete=models.SET_NULL , null=True , blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.user.email
    

class VideoSeriesHistory(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    #video_series = models.ForeignKey(VideoSeries , on_delete=models.SET_NULL, null=True , blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    
    