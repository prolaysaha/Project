from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.


def login_attempt(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(email = email).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/accounts/login/')
        
        

        user = authenticate(email = email , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/accounts/login/')
        
        login(request , user)
        return redirect('/')

    return render(request , 'auth/login.html')

def register_attempt(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        try:

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/accounts/register/')
            
            auth_token = str(uuid.uuid4())
            user_obj = User(email_token=auth_token ,email = email , first_name = first_name , last_name=last_name)
            user_obj.set_password(password)
            user_obj.save()
            
           
            send_mail_after_registration(email , auth_token)
            return redirect('/accounts/register/')


        except Exception as e:
            print(e)
            return redirect('/accounts/register/')
            


    return render(request , 'auth/register.html')

def success(request):
    return render(request , 'success.html')


def token_send(request):
    return render(request , 'token_send.html')



def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'error.html')


def logout_attempt(request):
    logout(request)
    return redirect('/')


def forget_password(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            
            
            if not User.objects.filter(email=email).first():
                messages.success(request, 'User not found with email.')
                return redirect('/accounts/forget-password/')
            
        
            user_obj = User.objects.filter(email=email).first()
            reset_token = str(uuid.uuid4())
            user_obj.forget_password_token = reset_token
            user_obj.save()
            messages.success(request, 'Email sent.')
            
            send_mail_for_reset_password(email , reset_token)
            
            return redirect('/accounts/forget-password/')
        
    except Exception as e:
        print(e)        
    return render(request , 'auth/change-password.html')


def confirm_forget_password(request, token):
    try:
        user_obj = User.objects.filter(forget_password_token = token).first()
        
        if not user_obj:
            return redirect('/error/')
        
        
        if request.method == 'POST':
            confirm_password = request.POST.get('password')
            reconfirm_password = request.POST.get('confirm_password')
           
            
            
    
                
            if confirm_password != reconfirm_password:
                messages.success(request, 'Both password and reconfirm password should be same.')
                return redirect(f'/accounts/forget-password/verify/{token}/')
              
    
            user_obj.set_password(confirm_password)
            user_obj.save()
            messages.success(request, 'Password changed.')

            return redirect('/accounts/login/')
            
                
    except Exception as e:
        print(e)
    
    
    return render(request , 'auth/confirm_forget_password.html' )

     


def send_mail_for_reset_password(email , token):
    subject = 'Your reset password link'
    message = f'Hi paste the link to reset password of  your account http://127.0.0.1:8000/accounts/forget-password/verify/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )
    
    



def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )
    