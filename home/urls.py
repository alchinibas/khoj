from django.urls import path,include
from . import views

app_name='home'
urlpatterns = [
    path('',views.index, name="index"),
    # path('result',views.result,name='result'),
    path('create',views.add_site,name='add_site'),
    path('result/load',views.loadData,name='load-data1'),
    path('olifros34594tu4g4g',views.loadRec,name='recommend'),
    path('asldifwef093je09ejrf',views.feedBack,name='feedback'),

    path('result',views.ResultView.as_view(),name='result'),
]
