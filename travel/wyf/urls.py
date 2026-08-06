from django.contrib import admin
from django.urls import path
from . import views

app_name = 'wyf'

urlpatterns = [
    path('part1',views.part1,name='part1'),
    path('part2',views.part2,name='part2'),
    path('part3',views.part3,name='part3'),
    path('part4',views.part4,name='part4'),
    path('part5',views.part5,name='part5'),
    path('part6',views.part6,name='part6'),
    path('get_cityData',views.get_cityData,name='get_cityData'),
]