
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls, name = "admin"),
    path('',include('home.urls')),
    path('khojadmin/',include('khojadmin.urls')),
]
