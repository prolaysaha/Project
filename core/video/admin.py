from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Category)
admin.site.register(Language)
admin.site.register(VideoSeries)
admin.site.register(VideoSeriesSections)
admin.site.register(SubscriptionType)