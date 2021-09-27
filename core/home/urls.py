
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
 
        path('' , home, name="home")  ,
        path('<id>/show-movies/' , show_movies , name="show_movies"),
        path('memberships/' , plans, name="plans"),
        path('profile/' ,profile, name="profile" ),
        path('success/' , success , name="success"),
        path('watch-now/<id>/' , watch_now , name="watch_now"),
        path('error/', error , name="error")
]
