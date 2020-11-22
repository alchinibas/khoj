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
# connect = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
connect = pymongo.MongoClient("localhost",27017)
db = connect["khoj"]
uncrawled = db["home_uncrawled"]
site = db["home_sitedetail"]
keyExtract = db["home_keyextract"]
Index = db["home_index"]
colkey = db["home_key"]
SiteRank = db["home_siterank"]
rankhandler = db["home_rankhandler"]

# ---------------------------------------------#


# ------Saves uncrawled urls---------
def Uncrawled(links):
    tmp=[]
    check = uncrawled.find({"url":{"$in":links}})
    if check:
        av = [i["url"] for i in check]
    tmp=[{"url":i,"ack":False} for i in links if i not in av and 'FalseURL' not in i]
    # for url in links:
    #     if 'False URL' not in url:
    #         check = uncrawled.find({'url': url})
    #         if not check:
    #             tmp.append({"url":url,"ack":False})
    uncrawled.insert_many(tmp)

# -----------Ranking Site --------------------

def InsertRank(siteid,url, urls, fu=False):

    def rank_inner(link,major=False):
        rnk = SiteRank.find_one({"url":link})

        if rnk :
            if not fu:
                if major and not rnk["site"]:
                    SiteRank.update_one({"url":link},{"$set":{"site":siteid},"$inc":{"rank":1}})
                    
                else:
                    SiteRank.update_one({"url":link},{"$inc":{"rank":1}})
            return rnk["_id"]

        else:
            if major:
                rnk1 = SiteRank.insert_one({"url":link,"site":siteid,"rank":1})
            else:
                rnk2 = 1 if not fu else 0
                rnk1 = SiteRank.insert_one({"url":link,"site":"","rank":rnk2})
            return rnk1.inserted_id
    if not fu:
        rank_inner(url,major=True)
    urlids = []
    for link in urls:
        urlids.append(rank_inner(link))
    if not fu:
        rankhandler.remove({"site":siteid})
        rankhandler.insert_one({"site":siteid,"links":urlids})
        # return SiteRank.find_one({"_id":rnk})["rank"]
    return urlids
    

#------------------------------------------------

#-------------UpdateRank---------------------

def UpdateRank(url,urlids):
    case1 = rankhandler.find_one({"site":url})
    if case1:
        links = [i for i in case1["links"]]
        new = urlids
        if links:
            old = [i for i in links if i not in urlids]
            if old:
                SiteRank.update_many({"_id":{"$in":old}},{"$inc":{"rank":-1}})
                rankhandler.update_many({"site":url},{"$pull":{"links":{"$in":old}}})
            new = [i for i in urlids if i not in links]
        if new:
            rankhandler.update_many({"site":url},{"$addToSet":{"links":{"$each":new}}})
            SiteRank.update_many({"_id":{"$in":new}},{"$inc":{"rank":1}})

# --------Saves site data---------------
def Sites(items,lang,urls):
    siteid=''
    db_check1 = site.find_one({"url":items['url']})
    if db_check1:
        if db_check1['word_links'] == items['words_links'] :
            print("This site exits in databae")
            return "The site exists in DB"
        else:
            siteid=db_check1["_id"]
            print("Site to be changed::",siteid)

            Index.update_many({"sites":siteid},{"$pull":{"sites":siteid}})
            keyExtract.delete_many({"file":siteid})
            urlids = InsertRank(siteid,items['url'],urls,fu=True)
            UpdateRank(siteid,urlids)

            site.update({"url":items['url']},{"$set":{
                "desc":items['description'][:100],
                "title": items['title'],
                "word_links": items['words_links'],
                "icon": items['icon'],
                }},upsert=False)
    else:
        site_detail = site.insert_one({
            "url":items['url'],
            "desc":items['description'][:100],
            "title": items['title'],
            "display": True,
            "visit_count": 0,
            "word_links": items['words_links'],
            "icon": items['icon'],
        })
        siteid=site_detail.inserted_id
        print("SIste created", siteid)
        InsertRank(siteid,items['url'],urls)
    uncrawled.delete_many({"url": items['url']})
    # print("site crawled and Deleting crawled::")
    if siteid:
        contents = items['description'].split()

        def index_core(target, priority,ktype):

            def key_cleaner(key):
                if items['lang']=='ne':
                    return key
                key = key.lower()
                if items['lang']=='en':
                    if re.match(r'^[a-z]+',key):
                        return key
                    elif re.match(r'.*\'.{0,1}$',key):
                        key = key[:key.rindex('\'')]
                return key

            def stop_word(word):
                words = ["in","the","is","was","were",
                "am","are","a","to","has","have","had","it"]
                if word in words:# include number  but not \w
                    return 1
                else:
                    if len(word)>1:
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
                    if exist_check:
                        exist= keyExtract.find_one({"key.value": ckey,"file":siteid}, {"original":0})
                        if exist:
                            start = exist["_id"]
                            keyExtract.update_one({"_id":exist["_id"]},{"$push":{
                                    "original":{"original":key,"ktype":ktype,"order":seq}
                                }},upsert=True)
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

def crawl(url):
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
        try:
            print('Crawling url: "%s" at depth: '% (url))
            headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.3",
                "From":"alchinbas123@gmail.com"
            }
            response = requests.get(url = url,headers = headers)
        except:
            print('Failed to perform HTTP GET request on "%s"\n' % url)
            uncrawled.delete_many({"url":url})
            return f'Failed to perform HTTP GET request on {url}'

        # accessing DNS file
        if response.status_code != 200:
            print("Failed with error:",response.status_code)
            return f'Failed error:{response.status_code}'

        content = BeautifulSoup(response.text, 'lxml')
        try:
            try:
                page_lang=content.find('html')['lang']
            except:
                page_lang='defalt'

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
                uncrawled.delete_one({"url":url})
                return "{'Error':" + e + ", 'URL':" + url + "}"

            tmp = [url['href'] for url in links]
            urls = [url_rebuild(url, base_url)
                    for url in set(tmp) if url not in crawled]
            print("No of links:::", len(urls))

            # -----------Updating/saving data

            current_desc_len = len(description.split())
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
            Uncrawled(urls)

        except Exception as e:
            print("No links avaliable. Error :", e)
            uncrawled.delete_many({"url":original})
            return f'Crawled success but no links available'
    else:
        uncrawled.delete_many({"url":url})
        return f'URL:{url} up to date'


def crawler(recursive=False):
    message = {}
    status = None

    def geturl():
        urls = uncrawled.find_one({"ack":True})
        if urls:
            link = urls['url']
            if not link:
                uncrawled.delete_many({"url":""})
                geturl()
            print("Source: " + link)
            return link
        else:
            
            return f'No links available'
    urlfind = geturl()
    if urlfind != "No links available":
        status = crawl(urlfind)
        message['message'] = status
    message['nexturl'] = geturl()

    if(recursive == True):
        status = crawler()

    return message
