from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import HttpResponse,Http404
from .includes import crawler
from home.models import uncrawled,feedback
import os
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    DetailView,
)
import pymongo as p
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from bson.objectid import ObjectId

con = p.MongoClient("localhost", 27017)
db = con.khoj
searchText = db.home_searchtext
Index = db.home_index
key = db.home_keyextract
fb = db.home_feedback
unc = db.home_uncrawled

@login_required
def adminAction(request):
    if request.method =='GET':
        if 'delete' in request.GET:
            pk = ObjectId(request.GET['delete'])
            obj = fb.delete_one({"_id":pk})
            if obj:
                messages.success(request,"Deleted Successfully!!!")
            else:
                raise Http404("Feedback Not Found")
            return redirect('khojadmin:feedback')
        elif 'check' in request.GET:
            pk = request.GET['check']
            obj=fb.update({"_id":ObjectId(pk)},{"$set":{"ack":True}})
            if obj:
                messages.success(request,"Marked Read Successfully!!!")
            else:
                messages.error(request,f"Failed to delete id :{pk}")
            return redirect('khojadmin:feedback')
        elif 'readSelected' in request.GET:
            data = request.GET['deleteSelected']
            if data:
                ids =json.loads(data)
                    #django sqlite command removed
                messages.success(request,"Selected messages deleted Successfully!!!")
            else:
                messages.warning(request,"No data selected")


            return redirect('khojadmin:feedback')
        elif 'deleteSelected' in request.GET:
            data = request.GET['readSelected']
            if data:
                ids=json.loads(data)

                #django sqlite command removed
                messages.success(request,"Selected messages marked read Successfully!!!")
            else:
                messages.warning(request,"No data selected")

            return redirect('khojadmin:feedback')
        elif 'aproveURL' in request.GET:
            url = request.GET['aproveURL']
            obj = unc.update({"url":url},{"$set":{"ack":True}})
            if obj:
                messages.success(request,f"Approved {url}")
            else:
                messages.error(request,f"Failed to update {url}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif 'rejectURL' in request.GET:
            url = request.GET['rejectURL']
            obj = unc.delete_many({"url":url})
            if obj:
                messages.success(request,f"URL Removed {url}")
            else:
                messages.error(request,f"Failed to update {url}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            raise PermissionDenied("403 Forbidden action access")
        return render(request, 'khojadmin/pendingurl.html')

    elif request.method=='POST':
        if request.POST['action'] == 'indexingurl':
            url=request.POST['url']
            if url:
                

                return HttpResponse("Internal Error")
            else:
                return HttpResponse("Failure")
        return HttpResponse("1")

@login_required
def crawl(request):
    status = crawler.crawler()

    return HttpResponse(json.dumps(status))

@login_required
def home(request):
    data = {
        "data":{
            "feedback":'',
            "sites":'',
            "uncrawled":'',
            "users":2343,
            "request":'',
        }
        
    }
    return render(request, 'khojadmin/index.html',context=data)

class LoginRequired:
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

class UrlRequests(LoginRequired,ListView):
    # model = uncrawled
    context_object_name = 'data'
    # ordering ='-requestDate'
    paginate_by = 20
    template_name='khojadmin/pendingurl.html'

    def get_queryset(self):
        urls = unc.find({"ack":False})
        return [i["url"] for i in urls]

@login_required
def dbms(request):
    return render(request, 'khojadmin/database.html')

class FeedbackView(LoginRequired, ListView):
    model = feedback
    template_name = 'khojadmin/feedback.html'
    context_object_name = 'data'
    paginate_by =5

    def get_queryset(self):
        dd = fb.find({})
        return [i for i in dd]


@login_required
def FeedbackDetail(request,pk):
    if request.method == 'GET':
        det = fb.find_one(ObjectId(pk))
        return render(request,'khojadmin/feedbackdetail.html',context = {"object":det})

@login_required
def dataManagement(request):
    return render(request,'khojadmin/dms.html')

@login_required
def report(request):
    return render(request,'khojadmin/report.html')

@login_required
def settings(request):
    return render(request, 'khojadmin/settings.html')


@login_required
def url_filter(request):
    return HttpResponse("Filtering body")