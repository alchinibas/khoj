from django.shortcuts import render
import json, math
from home.models import sites, indexing,search_text,feedback
from django.http import HttpResponse
from django.views.generic import ListView


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
        dat=search_text.objects.filter(search_text__contains = text).order_by('priority')
        for val in dat:
            data.append(val.search_text)

        return HttpResponse(', '.join(data))


def loadData(request):
    result=[]
    if request.method == 'GET':
        ids = [int(value) for value in request.GET['ids'].split(',')]
        for val in ids:
            q1= sites.objects.filter(pk=val)
            if(q1):
                result.append({'url':q1[0].url,'title':q1[0].title,'desc':q1[0].desc,'icon':q1[0].icon})
        comp=json.dumps(result)
        return render(request,'home/result_viewer.html',context={'result':result})


# def result(request,newsearch=True):
#     def resultprep(searchtext):
#         checkd=search_text.objects.filter(search_text=searchtext)
#         if len(checkd)>0:
#             checkd[0].visit_couont+=1
#             checkd[0].save()
#         else:
#             creater=search_text(search_text=searchtext)
#             creater.save()
#         keys=searchtext.split()
#         ids=[]
#         for key in keys:
#             search_result = indexing.objects.filter(key__contains=key)
#             for items in search_result:
#                 contents = json.loads(items.site_id,encoding="utf-8")
#                 for item in contents:
#                     ids.append(item['id'])
#         ids = list(set(ids))
#         key_str=json.dumps(ids,ensure_ascii=False)
#         request.session[searchtext]=key_str
#         print(request.session[searchtext])
#         return ids
#         # fn resultprep ends

#     if request.method == 'GET':
#         searchtext = request.GET['search-text']
#         if 'page' in request.GET:
#             try:
#                 page=int(request.GET['page'])
#             except:
#                 return HttpResponse("False Page Number")
#         else:
#             page=1
#         if searchtext not in request.session:
#             if searchtext == '':
#                 return render(request,'home/home_page.html')
#             ids=resultprep(searchtext)
#         else:
#             ids = json.loads(request.session[searchtext])
#         page_count=int(math.ceil(len(ids)/10))
#         ids = ids[(page-1)*10:page*10]
#         return render(request, 'home/result_page.html', context={'search': ids, 'search_text': searchtext,'page_count':page_count,'page':page})
#     else:
#         return HttpResponse("Failed to search.")


class ResultView(ListView):
    model = indexing
    template_name='home/result_page.html'
    context_object_name = 'search'
    paginate_by = 20

    def get_queryset(self):
        searchtext = self.request.GET['search-text']
        checkd=search_text.objects.filter(search_text=searchtext)
        if len(checkd)>0:
            checkd[0].visit_couont+=1
            checkd[0].save()
        else:
            creater=search_text(search_text=searchtext)
            creater.save()
        keys=searchtext.split()
        # ids=indexing.objects.none()
        ids = []
        for key in keys:
            for data in indexing.objects.filter(key__contains=key):
                for obj in json.loads(data.site_id):
                    ids.append(obj['id'])
        arrivals = sorted({i:ids.count(i) for i in set(ids)}.items(),key = lambda kv:kv[1], reverse=True)
        sorted_id = []
        for kv in arrivals:
            sorted_id.append(kv[0])
        return sorted_id

    def get_context_data(self, **kwargs):
        searchtext = self.request.GET['search-text']
        context = super().get_context_data(**kwargs)
        context['searchtext'] = searchtext
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


