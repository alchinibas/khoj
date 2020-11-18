from django.shortcuts import render
import json
from html import unescape
from home.models import Index,feedback
from django.http import HttpResponse
from django.views.generic import ListView
import pymongo as p


con = p.MongoClient("localhost", 27017)
db = con.khoj
searchText = db.home_searchtext
Index = db.home_index
key = db.home_keyextract


def index(request):
    return render(request, "home/home_page.html")


def loadRec(request):
    if request.method == 'GET':
        try:
            data=[]
            text=request.GET['text']
            if text=='':
                return HttpResponse(data)
        except :
            return HttpResponse()
        dat = searchText.find({"$text":{"$search":text}})
        # dat=search_text.objects.filter(search_text__contains = text).order_by('priority')
        if dat:
            for val in dat:
                data.append(val["search_text"])

        return HttpResponse(', '.join(data))


def loadData(request):
    result=[]
    if request.method == 'GET':
        result =json.loads("\""+unescape(request.GET['ids'])+"\"")
        # data = key.aggregate([{"$match":{""}}])
        print(result)
        comp=json.dumps(result)
        return render(request,'home/result_viewer.html',context={'result':result})


class ResultView(ListView):
    model = Index
    template_name = 'home/result_page.html'
    context_object_name = 'search'
    paginate_by = 20

    def get_queryset(self):
        searchtext = self.request.GET['search-text']
        checked = searchText.find_one({"search_text":searchtext})
        # checkd = search_text.objects.filter(search_text=searchtext)
        if checked:
            searchText.update({"search_text":searchtext,},{"$inc":{"visit_count":1}})
        else:
            searchText.insert_one({"search_text":searchtext,"visit_count":1,"priority":0})
        # keys = searchtext.split()
        '''Complex pymongo data search and match'''
        data = Index.aggregate([{"$match":{"$text":{"$search":searchtext}}},{"$unwind":"$sites"},{"$group":{"_id":"$sites","count":{"$sum":1}}},{"$lookup":{"from":"home_sitedetail","localField":"_id","foreignField":"_id","as":"sitedetail"}},{"$project":{"_id":1,"url":"$sitedetail.site.url","count":1}},{"$lookup":{"from":"home_siterank","localField":"url","foreignField":"site.url","as":"rank"}},{"$project":{"count":1,"rank":{"$first":"$rank.rank"}}},{"$sort":{"rank":-1,"count":-1}},{"$project":{"_id":1}}])
        return [i["_id"] for i in data]

    '''Adding search text in context'''
    def get_context_data(self, **kwargs):
        searchtext = self.request.GET['search-text']
        context = super().get_context_data(**kwargs)
        context['searchtext'] = searchtext
        print(len(context),context)
        return context



def add_site(request):
    with open("home/templates/home/test_file.json", "w") as j:
        cont = {
            "title": "Father",
            "summary": "A good man",
            "family": ["wife", "children"]
        }
        store = json.dumps(cont, indent=2)
        if (j.write(store)):
            return HttpResponse("Successful")
        else:
            return HttpResponse("Failed")


def feedBack(request):
    if request.method == 'POST':
        try:
            name=request.POST['name']
            email=request.POST['email']
            desc=request.POST['desc']
            q5= feedback(name=name, email=email, desc=desc)
            q5.save()
            if not q5:
                print("Failed TO save")
            # print(name,email,desc)

        except (KeyError,ValueError):
            return HttpResponse("False")
        else:

            return HttpResponse("True")

    else:
        print("Fuck this shit i am out")


