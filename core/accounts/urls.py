from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    
    path('register/' , register_attempt , name="register"),
    path('login/' , login_attempt , name="login"),
    path('token' , token_send , name="token_send"),
    path('success' , success , name='success'),
    path('verify/<auth_token>' , verify , name="verify"),
    path('error' , error_page , name="error"),
    path('forget-password/' , forget_password , name="forget_password"),
    path('logout/' ,logout_attempt , name="logout"),
    path('forget-password/verify/<token>/' , confirm_forget_password , name="confirm_forget_password"),

    
   
]
