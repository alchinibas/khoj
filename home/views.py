from django.shortcuts import render
import json
from home.models import sites, indexing,search_text,feedback
from django.http import HttpResponse


def index(request):
    return render(request, "home/home_page.html")


def loadRec(request):
    if request.method == 'GET':
        try:
            data=[]
            text=request.GET['text']
            if text=='':
                return HttpResponse(data)
            print(text)
        except :
            return HttpResponse()
        dat=search_text.objects.filter(search_text__contains = text).order_by('priority')
        for val in dat:
            data.append(val.search_text)

        return HttpResponse(', '.join(data))


def loadData(request):
    result=[]
    if request.method == 'GET':
        page=request.GET['page']
        for val in request.GET['ids'].split(','):
            q1= sites.objects.filter(pk=int(val))
            if(q1):
                result.append({'url':q1[0].url,'title':q1[0].title,'desc':q1[0].desc})
        comp=json.dumps(result)
        return render(request,'home/result_viewer.html',context={'result':result})


def result(request):
    if request.method == 'GET':
        searchtext = request.GET['search-text']
        checkd=search_text.objects.filter(search_text=searchtext)
        if len(checkd)>0:
            print(checkd[0])
            checkd[0].visit_couont+=1
            checkd[0].save()
        else:
            creater=search_text(search_text=searchtext)
            creater.save()
        keys=searchtext.split()
        ids=[]
        for key in keys:
            search_result = indexing.objects.filter(key__contains=key)
            for items in search_result:
                contents = json.loads(items.site_id,encoding="utf-8")
                for item in contents:
                    ids.append(item['id'])
        return render(request, 'home/result_page.html', context={'search': list(set(ids)), 'search_text': searchtext})
    else:
        return HttpResponse("Failed to search.")


def add_site(request):
    # try:
    #     with open('data.json','r') as j:
    #         cont=json.load(j)
    #         for data in cont:
    #             url=data[url]
    #             desc=data[desc]
    #             title=data[title]
    #             q=sites.object(url=url,desc=desc,title=title,)
    #             q.save()
    # except (FileNotFoundError):
    #     raise("File not not Found")
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
    print("Init Fe")
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
