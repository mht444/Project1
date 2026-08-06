from django.contrib import admin
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('',views.login),
    path('login',views.login,name='login'),
    path('register', views.register, name='register'),
    path('changeinfo',views.changeinfo,name='changeinfo'),
    path('upload_avatar', views.upload_avatar, name='upload_avatar'),
    path('logout', views.logout, name='logout'),
]