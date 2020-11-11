import json, os
import requests
from bs4 import BeautifulSoup
# from urllib import robotparser
import re
from .urlbreak import get_domain, url_rebuild
from home.models import sites, uncrawled, indexing

text_tags = ['p', 'h', 'div']
urls = []
growth = []
ses = []
tmp1 = []
tmp2 = []
domain = []
crawled = []

# ------Saves uncrawled urls---------
def Uncrawled(items):
    links = items['links']
    for url in links:
        check = uncrawled.objects.filter(url=url)
        if len(check) == 0 and 'False URL' not in url:
            q = uncrawled(url=url)
            q.save()


# --------Saves site data---------------
def Sites(items):
    current = sites(url=items['url'], title=items['title'], desc=items['description'][:255],
                    display=True, words_links=items['words_links'],icon = items['icon'])
    current.save()
    uncrawled.objects.filter(url = items['url']).delete()
    print("Deleting crawled::")
    if current:
        contents = items['description'].lower().split()

        def index_core(target,aid, priority):
            start = -1
            seq = 0
            try:
                for key in target:
                    q1 = indexing.objects.filter(key=key)
                    new_id = [{'id': aid, 'p': priority, aid:[start,],'sequence': [str(aid)+":"+str(seq),], 'count': 0}]
                    if len(q1) == 0:
                        reference_id = json.dumps(new_id, ensure_ascii=False)
                        q2 = indexing(key=key, site_id=reference_id,site_ids =json.dumps([aid,]))
                        if not q2:
                            print("failed")
                        q2.save()
                        start = q2[0].id
                        print("New Key generated::",key-q2[0].id)
                    else:
                        print("Preparing key edit::",key)
                        index_id = q1[0].id
                        ids = []
                        c = 0

                        ids = q1[0].site_id
                        try:
                            id_list = json.loads(ids)
                        except:
                            raise Exception("failed to parse data")
                        if q1[0].site_ids:
                            if aid not in json.loads(q1[0].site_ids):
                                id_list.append(new_id)
                            else:
                                for item in id_list:
                                    print(item)
                                    if item['id']==aid:
                                        item['count'] += 1
                                        item[str(aid)].append(start)
                                        item['sequence'].append(str(aid)+":"+str(seq))
                                        print(":::Changing key with available ids")
                        d_id = json.dumps(id_list, ensure_ascii=False)
                        q2 = indexing.objects.filter(id=index_id).update(site_id=d_id)
                        start = index_id

                    seq+=1
            except Exception as err:
                print("error ",err)

        index_core(contents,current.pk, 0)
        contents = items['title'].lower().split()
        index_core(contents,current.pk, 1)
        current.indexed = True
        current.save()
    else:
        print("Current variable not available")


def crawl(url, depth):
    print("Crawl started")
    original = url
    # Determining DNS
    if len(domain) == 0:
        url = get_domain(url)
    if re.match(r'^htt(p|ps)://[\w.]+/$', url):
        base_url = url
    else:
        base_url = get_domain(url=url, shrink=True)
    for link in domain:
        if base_url[6:] in link:
            base_url = link
            break
    if base_url not in domain:
        domain.append(base_url)
    try:
        # print("Base url:",base_url)
        # rp = robotparser.RobotFileParser()
        # rp.set_url(base_url + 'robots.txt')
        # rp.read()
        # check1 = rp.can_fetch("msnbot", url)
        # check2 = rp.can_fetch("*", url)
        data=requests.get(base_url+"/robots.txt",headers={"Content-Type":"text/plain"})

        data_sets = data.content.decode("utf-8").split("\r\n")
        check=True
        for items in data_sets:
            if items.startswith("Disallow"):
                block_path = items.split(":")[1].strip()
                if block_path in url:
                    check=False
    except:
        check = True
    if check:
        print("Crawl allowed:")
        try:
            print('Crawling url: "%s" at depth: %d' % (url, depth))
            response = requests.get(url)
        except:
            print('Failed to perform HTTP GET request on "%s"\n' % url)

            return f'Failed to perform HTTP GET request on {url}'

        # accessing DNS file

        content = BeautifulSoup(response.text, 'lxml')
        try:
            links = content.find_all('a', href=True)
            try:
                icon = content.find('link',attrs={'rel':'shortcut icon'})
                icon = icon['href']
                if icon.startswith("/"):
                    icon = base_url+icon
            except Exception as e:
                raise("False Icon",e)

            try:
                title = content.find('title').text
                for script in content(["script", "style", "footer", "button", "head",]):
                    script.extract()
                description = content.get_text()
                description = ' '.join(description.split())
                print("Description of %d words", len(description))
            except Exception as e:
                print("{'Error':"+e+", 'URL':"+url+"}")
                uncrawled.objects.filter(url=url).delete()
                return "{'Error':"+e+", 'URL':"+url+"}"

            # print('\n\nReturn:\n\n',json.dumps(result, indent=2))

            # urls=list(set([url['href'] for url in links]))
            tmp = [url['href'] for url in links]
            urls = [url_rebuild(url, base_url) for url in set(tmp) if url not in crawled]
            print("No of links:::",len(urls))
            # -----------Updating/saving data

            try:
                db_check1 = sites.objects.filter(url=url)
                desc_len = db_check1[0].words_links.split(':')[0]
                desc_links = db_check1[0].words_links.split(':')[1]
            except Exception as e:
                print("New data:")
                desc_len='0'
                desc_links = '0'
            current_desc_len = len(description.split())
            current_links = len(tmp)
            current_words_links = str(current_desc_len) +":"+ str(len(tmp))
            result = {
                'url': url,
                'title': title,
                'description': description,
                'words_links': current_words_links,
                'icon':icon,
            }
            if db_check1 and db_check1[0]:
                if desc_len == str(current_desc_len) and desc_links == str(current_links) and db_check1[
                    0].desc in description:
                    pass
                else:
                    db_check1[0].desc = description[:255]
                    db_check1[0].words_links = current_words_links
                q = uncrawled.objects.filter(url = url).delete();
                if q:
                    print("Re url deleted")
                else:
                    raise("Something is not right ")
                    #here left to update indexing /indexing available on Sites.index_core()

            else:
                Sites(result)

            if url not in crawled:
                crawled.append(url)
                if depth == 0:
                    tmp2 = [link for link in urls if link not in set(tmp1)]
                    for link in urls:
                        tmp1.append(link)
                    ses_dict = {
                        'from': url,
                        'links': tmp2,
                    }
                    Uncrawled(ses_dict)
                    return result
                print(str(len(urls)) + " anchor tags found")

                #For recursive crawling

                # c = 0
                # for link in urls:
                #     try:
                #         if 'False URL' not in url and c < 5:
                #             print("at : " + link)
                #             crawl(url=link, depth=depth - 1)
                #             c += 1
                #     except KeyError:
                #         pass

                return f'URL:{url} already visited'
        except Exception as e:
            print("No links avaliable. Error :",e)
            uncrawled.objects.filter(url=original).delete()
            return f'Crawled success but no links available'
    else:
        uncrawled.objects.filter(url= url).delete()
        return f'URL:{url} up to date'


def crawler(recursive = False):
    message = {}
    status = None
    def geturl():
        try:
            urls = uncrawled.objects.all()[:1]
            link = urls[0].url
            print("Source: " + link)
            return link
        except Exception:
            print("No links available to crawl")
            return "No links available to crawl"
    urlfind = geturl()
    if urlfind!="No links available to crawl":
        status = crawl(urlfind, depth=0)
        message['message'] = status
    message['nexturl'] = geturl()
   
    if(recursive == True):
        status = crawler()

    return message
