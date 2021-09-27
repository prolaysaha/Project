from django.db import models
from froala_editor.fields import FroalaField
# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=100)
    category_description = FroalaField()
    image = models.ImageField(upload_to="category")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.category
    
    
class Language(models.Model):
    language = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.language
    
    
class VideoSeries(models.Model):
    series_name = models.CharField(max_length=100)
    language = models.ForeignKey(Language , on_delete=models.CASCADE)
    #video_category = models.ForeignKey(Category , on_delete=models.CASCADE)
    video_category = models.ForeignKey(Category , on_delete=models.CASCADE)
    
    series_description = FroalaField()
    image = models.ImageField(upload_to="series")
    promo_video = models.FileField(upload_to="video" , null=True , blank=True)
    is_free = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.series_name    
    
class VideoSeriesSections(models.Model):
    video_series = models.ForeignKey(VideoSeries ,on_delete=models.CASCADE , null=True , blank=True)
    slug = models.CharField(max_length=100 ,null=True , blank=True)
    video_series_section_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="series" , null=True , blank=True)
    
    video = models.FileField(upload_to="video")
    can_watch = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.video_series_section_name
    
    
    
    
class SubscriptionType(models.Model):
    subsription_name = models.CharField(max_length=1000)
    subsription_days = models.IntegerField(default=0)
    subcription_price = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subsription_name
    
    
    
    
    

