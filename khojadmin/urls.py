from django.urls import path
from . import views

app_name='khojadmin'
urlpatterns=[
    path('crawl/',views.crawl, name='crawler'),
    path('',views.home,name="admin_home"),
    path('urlfilter/',views.url_filter, name='urlfilter'),
    path('dashboard/',views.home, name='admin_home'),
    path('sites/',views.SiteListView.as_view(),name='sites'),
    path('report/',views.report,name='report'),
    path('dataManagement/',views.dataManagement,name='dms'),
    path('feedback/',views.FeedbackView.as_view(),name='feedback'),
    path('urlrRquests/',views.UrlRequests.as_view(),name = 'urlrequests'),
    path('dataManagement/collections/',views.getcollection,name="collections"),
    path('094rjf09fj0wjf04yfsdhH()FE/',views.adminAction,name='adminaction'),
    path('feedback/<str:pk>',views.FeedbackDetail,name='feedbackdetail'),
    path('urlrRquests/aprovebydomain/',views.aprovebydomain,name='aprovebydomain'),
]
