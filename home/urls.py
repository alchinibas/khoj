from django.urls import path,include
from . import views

app_name='home'
urlpatterns = [
    path('',views.index, name="index"),
    path('result',views.result,name='result'),
    path('create',views.add_site,name='add_site'),
    path('result/load',views.loadData,name='load-data1'),
    path('olifros34594tu4g4g',views.loadRec,name='recommend'),
]
