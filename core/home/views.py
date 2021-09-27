from django.shortcuts import render
from video.models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from accounts.models import *
from django.contrib.auth.decorators import login_required
import datetime

from .helpers import *

def home(request):
    context = {}
    try:
        movie_series_objs = VideoSeries.objects.all().select_related('language' , 'video_category')
        
        if request.GET.get('search'):
            context['searched'] = True
            movie_series_objs = movie_series_objs.filter(series_name__icontains= request.GET.get('search'))
            
        if request.GET.get('category') and not request.GET.get('category') =='choose' :
            context['searched'] = True
            print(request.GET.get('category'))
            movie_series_objs = movie_series_objs.filter(video_category__in= request.GET.get('category'))
            
            
                    
        if request.GET.get('language') and not request.GET.get('language') =='choose':
            context['searched'] = True
            print(request.GET.get('language'))
            
            movie_series_objs = movie_series_objs.filter(language__in= request.GET.get('language'))
            
            
        
        
        
        context['movie_series_objs'] = movie_series_objs
        context['category'] = Category.objects.all()
        context['language'] = Language.objects.all()
    except Exception as e:
        print(e)
    return render(request ,'home.html' , context)


@login_required(login_url='/accounts/login/')
def show_movies(request , id):
    context = {}
    try:
        video_series = VideoSeries.objects.get(id = id)
        video_series_section = VideoSeriesSections.objects.filter(video_series=video_series)

        context["active_membership"] = SubscriptionHistory.objects.filter(user = request.user , subscription_end_date__gte= datetime.datetime.today()).first()        
        print( context["active_membership"])
        
        context['video_series'] = video_series
        context['video_series_sections'] = video_series_section
        
        
    except Exception as e:
        print(e)
        
    return render(request ,'show_movies.html' , context)


def error(request):
    return render(request , 'error.html')

@login_required(login_url='/accounts/login/')
def watch_now(request , id):
    context = {}
    
    if not subscription_checker(request):
        return render(request , 'error.html')
    
    video_series = VideoSeries.objects.get(id = id)
    video_series_section = VideoSeriesSections.objects.filter(video_series=video_series)
    
    
    if request.GET.get('section'):
        section_id = request.GET.get('current_video')
        current_video = VideoSeriesSections.objects.get(id=section_id).video
        current_image =   VideoSeriesSections.objects.get(id=section_id).image
    
    else:
        current_video = video_series.promo_video
        current_image = video_series.image
      
    
    context['current_video'] = current_video
    context['current_image'] = current_image   
       
        
    print(request.GET.get('section'))
    
    context["active_membership"] = SubscriptionHistory.objects.filter(user = request.user , subscription_end_date__gte= datetime.datetime.today()).first()

    
    context['video_series'] = video_series
    context['video_series_sections'] = video_series_section
    print(video_series_section)
    return render(request , 'watch_now.html' , context)


from django.conf import settings

def plans(request):
    context = { 'KEY_ID': settings.KEY_ID , 'KEY_SECRET' : settings.KEY_SECRET}    
    plans = []
    for plan in SubscriptionType.objects.all():
        result = {}
        result['id'] = plan.id
        result['subsription_name'] = plan.subsription_name
        result['subsription_days'] = plan.subsription_days
        result['subcription_price'] = plan.subcription_price
        result['is_active'] = plan.is_active
        result['created'] = plan.created
        
        order_amount = plan.subcription_price
        order_currency = 'INR'
        client = razorpay.Client(auth =(settings.KEY_ID  ,  settings.KEY_SECRET))
        
        payment = client.order.create({'amount':order_amount * 100, 'currency':'INR',
                              'payment_capture':'1' })
        result['order_id'] = payment['id']
        plans.append(result)
    
    context['plans'] = plans    
    
    
    
   # OPTIONAL

        
    
    return render(request , 'plans.html' , context)


@login_required(login_url='/accounts/login/')
def profile(request):
    
    context = {'memberships' : SubscriptionHistory.objects.filter(user = request.user)}
    
    return render(request , 'profile.html' , context)



def success(request):
    
    try:
        payment_id = request.GET.get('payment_id')
        order_id = request.GET.get('order_id')
        subcription_id = request.GET.get('subsription_id')
        
        subcription_obj = SubscriptionType.objects.get(id = subcription_id)
        
        subscription_history_obj = SubscriptionHistory(user=request.user)
        subscription_history_obj.is_active = True
        subscription_history_obj.order_id = order_id
        subscription_history_obj.razor_payment_id = payment_id
        subscription_history_obj.is_payment_successful = True
        subscription_history_obj.subscription_end_date = datetime.datetime.now() +  datetime.timedelta(days=subcription_obj.subsription_days)
        subscription_history_obj.subscription=subcription_obj
        subscription_history_obj.save()
        
    except Exception as e:
        print('@@@')
        print(e)
        print('@@@')
        
        
    
    return render(request , 'success.html')


    


