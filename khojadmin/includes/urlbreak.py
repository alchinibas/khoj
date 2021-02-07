import re


def get_domain(url, shrink=False):
    if re.match(r'^//', url):
        url = url[2:]
    if re.match(r'^http://', url) or re.match(r'^https://', url):
        val = url.index(':')
        n_st = url[val + 3:]
        http = url[:val + 3]
        if not shrink:
            return url_recheck(url)
        else:
            return http + extract(n_st)

    elif re.match(r'^www.', url):
        if shrink:
            return 'http://' + extract(url=url)
        else:
            return 'http://' + url_recheck(url)

    else:
        try:
            return url_recheck(url='http://www.' + url)
        except Exception:
            raise ("FalseURL:" + url)


def extract(url):
    if re.match(r'[\w\W]+/', url):
        return url[:url.index('/') + 1]

    elif not re.match(r'[\w\W]+/', url) and re.match(r'[\w\W]+?', url):
        if '?' in url:
            return url[:url.index('?')] + '/'
        else:
            return url+'/'


def url_recheck(url):
    if '?' not in url:
        if not re.match(r'[\w\W]+/$', url):
            return url + '/'
        else:
            return url
    else:
        return url


def url_rebuild(url, base_url):
    if re.match(r'^htt(p|ps)://[\w\W]+/?[\w\W]*', url):
        return url
    else:
        if re.match(r'^//', url):
            url = url[2:]

        if re.match(r'^/', url):
            return get_domain(url=base_url + url[1:], shrink=False)

        elif re.match(r'^\?', url):
            return get_domain(url=base_url[:-1] + url)
        elif re.match(r'^www', url):
            return 'http://' + url
        else:
            return "FalseURL:" + url
