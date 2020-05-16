from django.shortcuts import render
from django.http import HttpResponse
from .includes import crawler
from home.models import uncrawled, sites, indexing
import os, json


def home(request):
    return render(request, 'khojadmin/index.html')


def index(request):
    if os.path.exists('khoj_contents/content1'):
        print("Path Exists")
    try:
        q1 = sites.objects.filter(indexed=False)
        length = len(q1)
        print(str(length) + " files left to index")
        for items in q1:
            url = items.url
            f_name = items.reference_dir + '/' + items.file_name
            if os.path.exists(f_name):
                print("File Exists :" + f_name)
            else:
                print("File doesnt exists :" + f_name)
            try:
                with open(f_name, 'r', encoding='utf-8') as file:
                    contents = file.read().strip().split()
                for key in contents:
                    key = key.lower()
                    q1 = indexing.objects.filter(key=key)
                    new_id = [{"id": items.pk, "count": 0}]
                    if len(q1) == 0:
                        reference_id = json.dumps(new_id, ensure_ascii=False)
                        print("Indexing to :ref_id")
                        q2 = indexing(key=key, site_id=reference_id)
                        if not q2:
                            print("failed")
                        q2.save()
                    else:
                        index_id = q1[0].id
                        ids = []
                        c = 0

                        ids = q1[0].site_id
                        try:
                            id_list = json.loads(ids)
                        except:
                            raise Exception("failed to parse data")
                        for item in id_list:
                            if item['id'] != items.pk:
                                c = 0
                            else:
                                c = 1
                                break
                        if c == 0:
                            id_list.append({'id': items.pk, 'count': 0})
                        else:
                            item['count'] += 1
                        d_id = json.dumps(id_list, ensure_ascii=False)
                        q2 = indexing.objects.filter(id=index_id).update(site_id=d_id)
                # If indexing succeeds
                print("Indexed Complete: Removing File")
                ref_dir = items.reference_dir[14:]
                os.remove(f_name)
                print(ref_dir)
                q3 = reference_directory.objects.get(directory=ref_dir)
                q3.length -= 1
                print(q3.length)
                q3.save()
                q4 = sites.objects.filter(url=url).update(indexed=True)
            except FileNotFoundError:
                print("Failed to open File: " + f_name)
    except:
        print("Parsing Error")
    return HttpResponse("Process Complete")


def crawl(request):
    crawler.crawler()
    url_filter(request);
    return HttpResponse(url_filter(request))


def data_handler(request, action):
    if request.method == 'GET':
        if action == 'save':
            if os.path.exists('tmp_files/ses.json'):
                with open('tmp_files/ses.json', 'r', encoding='utf-8') as ses:
                    contents = json.load(ses, encoding='utf-8')
                    for items in contents:
                        links = items['links']
                        for url in links:
                            check = uncrawled.objects.filter(url=url)
                            if len(check) == 0 and 'False URL' not in url:
                                q = uncrawled(url=url)
                                q.save()
                os.remove('tmp_files/ses.json')
            if os.path.exists('tmp_files/data.json'):
                if os.stat("tmp_files/data.json").st_size > 2:
                    with open('tmp_files/data.json', encoding='utf-8') as data:
                        count=0
                        content = json.load(data)
                        for items in content:
                            dup = sites.objects.filter(url=items['url'])
                            q=[]
                            if len(dup) == 0:
                                print("Duplicate url found 0")

                                q = sites(url=items['url'], title=items['title'], desc=items['description'][:255],
                                          display=True)
                                q.save()
                            if q:
                               current=q
                            else:
                                current=dup[0]
                            if (current):
                                contents = items['description'].lower().split()

                                def index_core(target, priority):
                                    for key in target:
                                        q1 = indexing.objects.filter(key=key)
                                        new_id = [{'id': current.pk, 'p': priority, 'count': 0}]
                                        if len(q1) == 0:
                                            reference_id = json.dumps(new_id, ensure_ascii=False)
                                            q2 = indexing(key=key, site_id=reference_id)
                                            if not q2:
                                                print("failed")
                                            q2.save()
                                        else:
                                            index_id = q1[0].id
                                            ids = []
                                            c = 0

                                            ids = q1[0].site_id
                                            try:
                                                id_list = json.loads(ids)
                                            except:
                                                raise Exception("failed to parse data")
                                            for item in id_list:
                                                if item['id'] != current.pk:
                                                    c = 0
                                                else:
                                                    c = 1
                                                    break
                                            if c == 0:
                                                id_list.append({'id': current.pk,"p":priority, 'count': 0})
                                            else:
                                                item['count'] += 1
                                            d_id = json.dumps(id_list, ensure_ascii=False)
                                            q2 = indexing.objects.filter(id=index_id).update(site_id=d_id)
                                            print(indexing.objects.filter(key=key)[0].site_id)
                                index_core(contents,0)
                                contents=items['title'].lower().split()
                                index_core(contents,1)
                                current.indexed=True
                                current.save()
                os.remove('tmp_files/data.json')
        elif action == 'arrange_files':
            if not os.path.exists('khoj_contents'):
                os.makedirs('khoj_contents')
                reference_directory(directory='khoj_contents', category=1, length=1).save()
                os.makedirs('khoj_contents/content1')
                reference_directory(directory='content1', length=0).save()
            else:
                return HttpResponse(dir_handler())
    return HttpResponse("Completed")


def dir_handler():
    try:
        lo = reference_directory.objects.filter(length__lt=1000, category=10)
        return lo[0].directory
    except (reference_directory.DoesNotExist, IndexError):
        lo = len(reference_directory.objects.all())
        name1 = 'content' + str(lo)
        name = 'khoj_contents/' + name1
        os.makedirs(name)
        q = reference_directory(directory='content' + str(lo))
        q.save()
        try:
            q = reference_directory.objects.get(directory='khoj_contents')
            q.length += 1
            q.save()
        except:
            print("Fatal Error")
        return name1


def url_filter(request=False):
    crawled_data = sites.objects.values_list('url')
    crawled = [url[0] for url in crawled_data]
    print("Removing duplicates from uncrawled")
    for items in crawled:
        try:
            q3=uncrawled.objects.filter(url=items).delete()
            print(uncrawled.objects.filter(url=items))
        except sites.DoesNotExists:
            pass
        except:
            print("Something is not right")
    print("Removing false url")
    x = 'URL duplicates removed'
    try:
        uncrawled.objects.filter(url__startswith="False URL:").delete()
    except:
        x = "No False URL Exists"
    return x
