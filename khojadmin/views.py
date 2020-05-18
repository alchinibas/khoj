from django.shortcuts import render
from django.http import HttpResponse
from .includes import crawler
from home.models import uncrawled, sites, indexing
import os
import json


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
                        c = 0

                        ids = q1[0].site_id
                        try:
                            id_list = json.loads(ids)
                        except Exception:
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
                        indexing.objects.filter(id=index_id).update(site_id=d_id)
                # If indexing succeeds
                print("Indexed Complete: Removing File")
                ref_dir = items.reference_dir[14:]
                os.remove(f_name)
                print(ref_dir)
                sites.objects.filter(url=url).update(indexed=True)
            except FileNotFoundError:
                print("Failed to open File: " + f_name)
    except Exception as e:
        print("Parsing Error")
    return HttpResponse("Process Complete")


def crawl(request):
    crawler.crawler()
    url_filter(request)
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
                        content = json.load(data)
                        for items in content:
                            dup = sites.objects.filter(url=items['url'])
                            q = []
                            if len(dup) == 0:
                                print("Duplicate url found 0")

                                q = sites(url=items['url'], title=items['title'], desc=items['description'][:255],
                                          display=True)
                                q.save()
                            if q:
                                current=q
                            else:
                                current=dup[0]
                            if current:
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
                                index_core(contents,0)
                                contents=items['title'].lower().split()
                                index_core(contents,1)
                                current.indexed=True
                                current.save()
                os.remove('tmp_files/data.json')
        elif action == "indexfilter":
            sids=[]
            iids=[]
            print("Determining unwanted indexes")
            allsites=sites.objects.all()
            for objects in allsites:
                sids.append(objects.pk)
            for objects in indexing.objects.all():
                keys = objects.site_id
                keygroup=json.loads(keys, encoding = 'utf-8')
                for items in keygroup:
                    if(items['id'] not in sids):
                        iids.append(items['id'])
                        try:
                            keygroup.remove(items)
                            indexing.objects.filter(key = objects.key).update(site_id = json.dumps(keygroup, ensure_ascii= False))
                        except Exception as e:
                            print(e)

                iids = list(set(iids))
            print("Unwanted ids : ", iids)
    return HttpResponse("Completed")


def url_filter(request):
    chk=0
    crawled_data = sites.objects.values_list('url')
    crawled = [url[0] for url in crawled_data]
    print("Removing duplicates from uncrawled")
    for items in crawled:
        try:
            q3=uncrawled.objects.filter(url=items)
            sit=q3[0].url
            q4=q3.delete()
            chk=1
            if q4:
                print(sit)
            else:
                print("Failed removing url:",items)
        except sites.DoesNotExist:
            print("New URL : ", items)
        except:
            pass
    print("Removing false url")
    x = 'URL duplicates removed'
    try:
        uncrawled.objects.filter(url__startswith="False URL:").delete()
    except:
        x = "No False URL Exists"
    if chk and chk== 1:
        print("Checking Again:::")
        url_filter(request)
    else:
        print("Finished Checking")
        if 'afc' in request.GET:
            return HttpResponse(x)
        else:
            return x
