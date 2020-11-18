import json
import os
import requests
from bs4 import BeautifulSoup
# from urllib import robotparser
import re
from .urlbreak import get_domain, url_rebuild
# from bson.objectid import ObjectId
import pymongo


text_tags = ['p', 'h', 'div']
urls = []
growth = []
ses = []
tmp1 = []
tmp2 = []
domain = []
crawled = []
stop_words = []
page_lang = 'default'
# ----------Requetion Dabatase nd Collections-------------
connect = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = connect["khoj"]
uncrawled = db["home_uncrawled"]
site = db["home_sitedetail"]
keyExtract = db["home_keyextract"]
Index = db["home_index"]
colkey = db["home_key"]
SiteRank = db.home_siterank
rankhandler = db.home_rankhandler

# ---------------------------------------------#


# ------Saves uncrawled urls---------
def Uncrawled(items):
    links = items['links']
    for url in links:
        check = uncrawled.find({'url': url})
        if not check and 'False URL' not in url:
            q = uncrawled.insert_one({'url': url})

# -----------Ranking Site --------------------

def InsertRank(url, urls, fu=False):

    def rank_inner(url):
        rnk = SiteRank.find_one({"site.url":url})
        if rnk :
            if not fu:
                SiteRank.update_one({"site.url":url},{"$inc":{"rank":1}})
            return rnk["_id"]

        else:
            rnk1 = SiteRank.insert_one({"site":{"url":url},"rank":1})
            return rnk1.inserted_id
    if not fu:
        rnk = rank_inner(url)
    urlids = []
    for link in urls:
        urlids.append(rank_inner(link))
    if not fu:
        rankhandler.remove({"url":url})
        rankhandler.insert_one({"url":url,"links":urlids})
        return SiteRank.find_one({"_id":rnk})["rank"]
    return urlids
    

#------------------------------------------------

#-------------UpdateRank---------------------

def UpdateRank(url,urlids):
    case1 = rankhandler.find_one({"url":url})
    if case1:
        links = [i for i in case1["links"]]
        new = urlids
        if links:
            old = [i for i in links if i not in urlids]
            if old:
                SiteRank.update_many({"site.url":{"$in":old}},{"$inc":{"rank":-1}})
                rankhandler.update_many({"url":url},{"$pull":{"links":{"$in":old}}})
            new = [i for i in urlids if i not in links]
        if new:
            rankhandler.update_many({"url":url},{"$addToSet":{"links":{"$each":new}}})

# --------Saves site data---------------
def Sites(items,lang,urls):
    site_detail = 1
    db_check1 = site.find_one({"site.url":items['url']})
    if db_check1:
        if db_check1['word_links'] == items['words_links'] :
            print("This site exits in databae")
            return "The site exists in DB"
        else:
            siteid=db_check1["_id"]
            print("Site to be changed::",siteid)

            Index.delete_many({"sites":siteid})
            keyExtract.delete_many({"file":siteid})
            urlids = InsertRank(items['url'],urls,fu=True)
            UpdateRank(items['url'],urlids)
            site.update({"site.url":items['url']},{"$addToSet":{
                "desc":items['description'][:100],
                "title": items['title'],
                "visit_count": 0,
                "word_links": items['words_links'],
                "icon": items['icon'],
                }},upsert=True)
    else:
        # SiteRank.insert_one({"site":{"url":items['url']},"rank":1.0})
        p = InsertRank(items['url'],urls)
        site_detail = site.insert_one({
            "site": {"url": items['url']},
            "desc":items['description'][:100],
            "title": items['title'],
            "domain": ".com",
            "display": True,
            "visit_count": 0,
            "priority":p,
            "indexed": True,
            "word_links": items['words_links'],
            "icon": items['icon'],
        })
        siteid=site_detail.inserted_id
    # uncrawled.delete_many({"url": items['url']})
    # print("site crawled and Deleting crawled::")
    if site_detail:
        contents = items['description'].split()

        def index_core(target, priority,ktype):

            def key_cleaner(key):
                key = key.lower()
                if items['lang']=='en':
                    if re.match(r'^[a-z]+',key):
                        return key
                    elif re.match(r'.*\'.{0,1}$',key):
                        key = key[:key.rindex('\'')]
                return key

            def stop_word(word):
                words = ["in","the","is","was","were",
                "am","are","a","to","has","have","had"]
                if word in words:# include number  but not \w
                    return 1
                else:
                    if len(word)>2:
                        if word.isalnum():
                            return 0
                    elif  word.isalpha():
                        return 1

                    return 1

            start = ''
            prev_key=''
            seq = 0
            for i,key in enumerate(target):
                ckey = key_cleaner(key)
                # print("Cleanded ::",ckey)
                check_stop_word = stop_word(ckey)
                # print("Kye ::",ckey)
                if check_stop_word:
                    if (i+1) != len(target):
                        stop_words.append(key)
                    else:
                        if prev_key:
                            key = prev_key+" "+" ".join(stop_words)+" "+key
                            keyExtract.update_one({"_id":start,
                                "original":{"$elemMatch":{
                                    "ktype":ktype,"order":seq
                                }}},{"$pop":{"original":1
                                }})
                            keyExtract.update_one({"_id":start},
                                {"$push":{
                                    "original":{
                                        "original":key,"ktype":ktype,"order":seq
                                    }}},upsert=True)
                else:
                    seq+=1
                    if stop_words:
                        key = " ".join(stop_words)+" "+key
                        stop_words.clear()
                    exist_check = Index.find_one({"_id": ckey},{"sites":0})
                    # if exist_check:
                        # start = exist_check["_id"]
                    if exist_check:
                        exist= keyExtract.find_one({"key.value": ckey,"file":siteid}, {"original":0})
                        # print("Exist value",exist)
                        if exist:
                            start = exist["_id"]
                            # original = exist['index'][0]['original']
                            # pre_keys=exist['index'][0]['previous_keys']
                            # priority=exist['index'][0]['priority']
                            # print("Updating existing index")
                            keyExtract.update_one({"_id":exist["_id"]},{"$push":{
                                    "original":{"original":key,"ktype":ktype,"order":seq}
                                }},upsert=True)
                            #priority set by dictionary importance

                            # pre_keys.append({"key":start})
                        else:
                            ind = keyExtract.insert_one({"key":{"value":ckey},
                                "original":[{"original":key,"ktype":ktype,"order":seq}],
                                "file":siteid
                                })
                            start = ind.inserted_id
                            Index.update_one({"_id":exist_check["_id"]},{"$push":{
                                "sites":siteid
                                }})
                    else:
                        # print("New Key/ Found",ckey)
                        ind = keyExtract.insert_one({
                            "key":{"value":ckey},
                            "original":[{"original":key,"ktype":ktype,"order":seq}],
                            "file":siteid
                            })
                        start = ind.inserted_id
                        Index.insert_one({ 
                            "_id":ckey,
                            "sites":[siteid]
                            })

                prev_key=key
        index_core(contents, 0.000,"body")
        contents = items['title'].lower().split()
        index_core(contents, 1.000,"title")
    else:
        print("Current variable not available")

def crawl(url, depth):
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
    headers = {
        "User-Agent":"Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36",
        "From":"alchinbas123@gmail.com"
    }
    try:
        # print("Base url:",base_url)
        # rp = robotparser.RobotFileParser()
        # rp.set_url(base_url + 'robots.txt')
        # rp.read()
        # check1 = rp.can_fetch("msnbot", url)
        # check2 = rp.can_fetch("*", url)
        data = requests.get(url = base_url + "/robots.txt",
                            headers=headers.update({"Content-Type": "text/plain"}))

        data_sets = data.content.decode("utf-8").split("\r\n")
        check = True
        for items in data_sets:
            if items.startswith("Disallow"):
                block_path = items.split(":")[1].strip()
                if block_path in url:
                    check = False
    except:
        check = True
    if check:
        print("Crawl allowed:")
        try:
            print('Crawling url: "%s" at depth: %d' % (url, depth))
            headers = {
                "User-Agent":"Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36",
                "From":"alchinbas123@gmail.com"
            }
            response = requests.get(url = url,headers = headers)
        except:
            print('Failed to perform HTTP GET request on "%s"\n' % url)

            return f'Failed to perform HTTP GET request on {url}'

        # accessing DNS file
        if response.status_code != 200:
            print("Failed with error:",response.status_code)
            return f'Failed error:{response.status_code}'

        content = BeautifulSoup(response.text, 'lxml')
        try:
            page_lang=content.html['lang']
            links = content.find_all('a', href=True)
            try:
                icon = content.find('link', attrs={'rel': 'shortcut icon'})
                icon = icon['href']
                if icon.startswith("/"):
                    icon = base_url + icon
            except Exception as e:
                print("False Icon", e)

            try:
                title = content.find('title').text
                for script in content(["script", "style", "footer", "button", "head", ]):
                    script.extract()
                description = content.get_text()
                description = ' '.join(description.split())
                print("Description of %d words", len(description))
            except Exception as e:
                print("{'Error':" + e + ", 'URL':" + url + "}")
                # uncrawled.objects.filter(url=url).delete()
                uncrawled.delete_one({"url":url})
                return "{'Error':" + e + ", 'URL':" + url + "}"

            # print('\n\nReturn:\n\n',json.dumps(result, indent=2))

            # urls=list(set([url['href'] for url in links]))
            # print("ReBuilding URL")
            tmp = [url['href'] for url in links]
            urls = [url_rebuild(url, base_url)
                    for url in set(tmp) if url not in crawled]
            print("No of links:::", len(urls))

            # -----------Updating/saving data

            current_desc_len = len(description.split())
            current_links = len(tmp)
            current_words_links = str(current_desc_len) + ":" + str(len(tmp))
            # print("Current word link/s",current_words_links)
            result = {
                'url': url,
                'title': title,
                'description': description,
                'words_links': current_words_links,
                'icon': icon,
                'lang':page_lang,
            }

            Sites(result,page_lang,urls)

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

                return f'URL:{url} already visited'
        except Exception as e:
            print("No links avaliable. Error :", e)
            # uncrawled.delete_many({"url":original})
            return f'Crawled success but no links available'
    else:
        uncrawled.delete_many({"url":url})
        return f'URL:{url} up to date'


def crawler(recursive=False):
    message = {}
    status = None

    def geturl():
        try:
            urls = uncrawled.find_one()
            link = urls['url']
            print("Source: " + link)
            return link
        except Exception:
            # print("No links available to crawl")
            return "No links available to crawl"
    urlfind = geturl()
    if urlfind != "No links available to crawl":
        status = crawl(urlfind, depth=0)
        message['message'] = status
    message['nexturl'] = geturl()

    if(recursive == True):
        status = crawler()

    return message
