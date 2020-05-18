from django.urls import path
from . import views

app_name='khojadmin'
urlpatterns=[
    path('crawl/',views.crawl, name='crawler'),
    path('index/',views.index,name='indexer'),
    path('data_handler/<str:action>/',views.data_handler,name='data_handler'),
    path('',views.home,name="admin_home"),
    path('urlfilter/',views.url_filter, name='urlfilter'),
]
