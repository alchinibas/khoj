from django.shortcuts import render
import json
from html import unescape
from home.models import feedback
from django.http import HttpResponse
from django.views.generic import ListView
import pymongo as p
from bson.objectid import ObjectId
from django.utils import timezone

con = p.MongoClient("localhost", 27017)
db = con.khoj
searchText = db.home_searchtext
Index = db.home_index
key = db.home_keyextract
fb = db.home_feedback

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
        dat = searchText.find({"$text":{"$search":text}}).limit(10)
        # dat=search_text.objects.filter(search_text__contains = text).order_by('priority')
        if dat:
            for val in dat:
                data.append(val["search_text"])

        return HttpResponse(', '.join(data))


def loadData(request):
    result=[]
    if request.method == 'GET':
        result =[ObjectId(i) for i in json.loads(unescape(request.GET['ids']).replace("'","\""))]
        # result = request.GET['ids']
        text = request.GET['searchtext']
        print(result,text)
        data = key.aggregate([
            {"$match":{"$text":{"$search":text},"file":{"$in":result}}},
            {"$unwind":"$original"},
            {"$match":{"original.ktype":"body"}},
            {"$sort":{"original.order":1}},
            {"$group":{"_id":"$file","file":{"$first":"$file"},"keys":{"$push":"$original"}}},
            {"$project":{"_id":0,"file":1,"keys":{"$slice":["$keys",3]}}},
            {"$unwind":"$keys"},
            {"$lookup":{"from":"home_keyextract","let":{"site":"$file","ord":"$keys"},"pipeline":[
                {"$match":{"$expr":{"$eq":["$file","$$site"]}}},
                {"$unwind":"$original"},
                {"$match":{"original.ktype":"body","$expr":{"$and":[
                    {"$gt":["$original.order",{"$sum":["$$ord.order",-25]}]},
                    {"$lt":["$original.order",{"$sum":["$$ord.order",25]}]}
                ]}}},
                {"$sort":{"original.order":1}},
                {"$group":{"_id":"$file","content":{"$push":"$original"}}},
                {"$project":{"_id":0,"value":"$content"}}
                ],"as":"content"}},
            {"$unwind":"$content"},
            {"$lookup":{
                "from":"home_sitedetail","localField":"file","foreignField":"_id","as":"site"}
            },{"$unwind":"$site"},
            {"$group":{"_id":"$file","content":{"$push":"$content"},"url":{"$first":"$site.url"},"title":{"$first":"$site.title"}}},
            ])
        result = []
        for i in data:
            tmp=[]
            for j in i["content"]:
                for k in j["value"]:
                    tmp.append(k) if k not in tmp else False
            i["content"]=' '.join([t["original"] for t in tmp])[:250]
            result.append(i)
        return render(request,'home/result_viewer.html',context={'result':result})


class ResultView(ListView):
    model = Index
    template_name = 'home/result_page.html'
    context_object_name = 'search'
    paginate_by = 20

    def get_queryset(self):
        searchtext = self.request.GET['search-text']
        checked = searchText.find_one({"search_text":searchtext})
        if checked:
            searchText.update({"search_text":searchtext,},{"$inc":{"visit_count":1}})
        else:
            searchText.insert_one({"search_text":searchtext,"visit_count":1,"priority":0})
        '''Complex pymongo data search and match'''
        data = Index.aggregate([
            {"$match":{"$text":{"$search":searchtext}}},
            {"$addFields":{"score":{"$meta":"textScore"}}},
            {"$unwind":"$sites"},
            {"$group":{"_id":"$sites","count":{"$sum":1},"score":{"$sum":"$score"}}},
            {"$lookup":{"from":"home_siterank","localField":"_id","foreignField":"site","as":"rank"}},
            {"$project":{"count":"$count","score":"$score","ranke":{"$first":"$rank.rank"}}},
            {"$project":{"count":"$count","ranke":"$ranke","score":"$score","trank":{"$add":["$count","$ranke","$score"]}}},
            {"$sort":{"trank":-1}}])
        return [str(i["_id"]) for i in data]

    '''Adding search text in context'''
    def get_context_data(self, **kwargs):
        searchtext = self.request.GET['search-text']
        context = super().get_context_data(**kwargs)
        context['searchtext'] = searchtext
        # print(len(context),context)
        return context


def feedBack(request):
    if request.method == 'POST':
        try:
            name=request.POST['name']
            email=request.POST['email']
            desc=request.POST['desc']
            q5= fb.insert_one({"name":name,"email":email,"desc":desc,"report_date":timezone.now(),"ack":False})
            if not q5:
                print("Failed TO save")
            

        except (KeyError,ValueError):
            return HttpResponse("False")
        else:

            return HttpResponse("True")

    else:
        print("i am out")
        return "Wrong RequestMethod"


def aboutus(request):
    return render(request,'home/about_us.html')