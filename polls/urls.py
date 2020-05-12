from django.urls import path
from . import views

urlpatterns=[
    path('',views.index, name='polls_index'),
    path('result/',views.result,name='result'),
]
