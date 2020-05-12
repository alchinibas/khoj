from django.shortcuts import render
from django.http import HttpResponse
from home.models import indexing, sites

def index(request):
    return HttpResponse("This is polls index page")

def result(request):
    if(request.method=='GET'):
        search=request.GET['search-text']
        search =sites.objects.get(desc__contains=search)
        return render(request, 'home/result.html',context={'search':search})
    else:
        return HttpResponse("Failed to searach.")
