import json
import requests
from bs4 import BeautifulSoup
from urllib import robotparser
import re
from .urlbreak import get_domain, url_rebuild
from home.models import sites, uncrawled

text_tags = ['p', 'h', 'div']
data = []
urls = []
growth = []
ses = []
tmp1 = []
tmp2 = []
domain = []
crawled = []
print("Load crawled urls")
sites_data = sites.objects.values_list('url')
for items in sites_data:
    crawled.append(items[0])


def crawl(url, depth):
    original=url
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
        rp = robotparser.RobotFileParser()
        rp.set_url(base_url + 'robots.txt')
        rp.read()
        check1 = rp.can_fetch("msnbot", url)
        check2 = rp.can_fetch("*", url)
    except:
        check1 = True
        check2 = True
    if check2 or check1:
        try:
            print('Crawling url: "%s" at depth: %d' % (url, depth))
            response = requests.get(url)
        except:
            print('Failed to perform HTTP GET request on "%s"\n' % url)
            return

        # accessing DNS file

        content = BeautifulSoup(response.text, 'lxml')
        try:
            links = content.find_all('a', href=True)
            try:
                title = content.find('title').text
                description = ''
                for script in content(["script", "style", "footer","a", "button", "head", "meta"]):
                    script.extract()
                description = content.get_text()
                description = ' '.join(description.split())
                print("Description of %d words", len(description))
            except:
                return

            result = {
                'url': url,
                'title': title,
                'description': description
            }
            # print('\n\nReturn:\n\n',json.dumps(result, indent=2))

            # urls=list(set([url['href'] for url in links]))
            tmp = []
            tmp = [url['href'] for url in links]
            urls = [url_rebuild(url, base_url) for url in set(tmp) if url not in crawled]

            if result not in data:
                data.append(result)
                if depth == 0:
                    tmp2 = [link for link in urls if link not in set(tmp1)]
                    for link in urls:
                        tmp1.append(link)
                    ses_dict = {
                        'from': url,
                        'links': tmp2
                    }
                    ses.append(ses_dict)
                    return "Returned 1"
                print(str(len(urls)) + " anchor tags found")
                c = 0
                for link in urls:
                    try:
                        if 'False URL' not in url and c < 5:
                            print("at : " + link)
                            crawl(url=link, depth=depth - 1)
                            c += 1
                    except KeyError:
                        pass

                return
        except:
            print("No links avaliable")
            q5=uncrawled.objects.filter(url=original).delete()
            return
    else:
        return


def crawler():
    try:
        urls = uncrawled.objects.all()[:1]
        link = urls[0].url
        print("Source: " + link)
    except Exception:
        print("Failed : Either no links to crawl or error in database connection")
        return
    crawl(link, depth=2)
    with open("tmp_files/data.json", "w", encoding="utf-8") as json_file:

        file_content = (json.dumps(data, indent=2, ensure_ascii=False))
        json_file.write(file_content)

    print('length of data:', len(data))

    with open("tmp_files/ses.json", "w", encoding="utf-8") as json_ses:
        list_json = json.dumps(ses, indent=2, ensure_ascii=False)
        json_ses.write(list_json)
    return
