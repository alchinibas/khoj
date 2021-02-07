from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import HttpResponse,Http404
from .includes import crawler
from home.models import uncrawled,feedback
import os
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
import pymongo as p
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from bson.objectid import ObjectId
from khojadmin.includes import urlbreak

con = p.MongoClient("localhost", 27017)
db = con.khoj
searchText = db.home_searchtext
Index = db.home_index
key = db.home_keyextract
fb = db.home_feedback
unc = db.home_uncrawled
site = db.home_sitedetail
user = db.auth_user
rank = db.home_siterank
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
                q2 = rank.find_one({"url":{"$regex":url+".*"}})
                if not q2:
                    q1 = unc.find_one({"url":{"$regex":url+".*"}})
                    if not q1:
                        unc.insert_one({"url":url,"ack":False}) 
                        return HttpResponse("True")
                return HttpResponse("URL already waiting for aproval")
            else:
                return HttpResponse("Failure")
        return HttpResponse("1")

@login_required
def crawl(request):
    status = crawler.crawler()

    return HttpResponse(json.dumps(status))

@login_required
def home(request):
    data ={
            "feedback":fb.count_documents({}),
            "sites":site.count_documents({}),
            "uncrawled":unc.count_documents({}),
            "users":user.count_documents({}),
            "pending":unc.count_documents({"ack":True}),
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
        query = {"ack":False}
        if 'search' in self.request.GET:
            gturl = self.request.GET['search']
            print(gturl,"received url")
            reg = ".*"+gturl+".*"
            print(reg)
            query = {"url":{"$regex":reg},"ack":False}
        urls = unc.find(query)
        return [i["url"] for i in urls]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'search' in self.request.GET:
            searchtext = self.request.GET['search']
            context['searchtext'] = searchtext
        # print(len(context),context)
        return context


@login_required
def aprovebydomain(request):
    if request.method == 'POST':
        url = request.POST['url']
        base_url = urlbreak.get_domain(url=url,shrink=True)
        if 'FalseURL' not in base_url:
            count = unc.count_documents({"url":{"$regex":base_url+".*"}})
            change = unc.update_many({"url":{"$regex":base_url+".*"}},{"$set":{"ack":True}})
            messages.success(request,f"Count {count}, updated {change.matched_count}")
        return redirect('khojadmin:urlrequests')
    raise Http404("Request Response not found")


class SiteListView(LoginRequired,ListView):
    template_name = 'khojadmin/sites.html'
    context_object_name = 'data'
    paginate_by = 20
    
    def get_queryset(self):
        if 'search' in self.request.GET:
            searchtext = self.request.GET['search']
            data = site.find({"url":{"$regex":".*"+searchtext+".*"}})
        else:
            data = site.find({})
        return [i for i in data]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'search' in self.request.GET:
            searchtext = self.request.GET['search']
            context['searchtext'] = searchtext
        # print(len(context),context)
        return context


@login_required
def getcollection(request):
    def getobject(col):
        act_col = db.get_collection(col)
        return act_col
    if 'truncate' in request.GET:
        print("Truncate reuqeted")
        col = request.GET['truncate']
        obj = getobject(col)
        if obj:
            q6 = obj.delete_many({})
            if q6:
                messages.success(request,f"Successfully  Truncated col: {col}")
            else:
                messages.error(request,f"Failed to truncate col: {col}")
        else:
            messages.warning(request,f"No collection found name: {col}")
    dbs = db.list_collection_names()
    tmp=[]
    for coln in dbs:
        colnm =getobject(coln)
        count = colnm.count_documents({})
        tmp.append({"name":coln,"count":count})
    return render(request,'khojadmin/collection.html',context = {"dbs":tmp})

class FeedbackView(LoginRequired, ListView):
    model = feedback
    template_name = 'khojadmin/feedback.html'
    context_object_name = 'data'
    paginate_by =5

    def get_queryset(self):
        dd = fb.find({}).sort("ack",1)
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