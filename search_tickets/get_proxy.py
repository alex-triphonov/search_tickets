import requests
from requests.exceptions import SSLError
from urllib3.exceptions import MaxRetryError
import random
from bs4 import BeautifulSoup

usr_agent = [
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36'
]


def check_validation(proxy):
    try:
        r = requests.get('https://www.facebook.com/', proxies=proxy, timeout=2)
    except (SSLError, MaxRetryError):
        return False
    if r.status_code == 200:
        return True
    return False


def get_proxies():
    s = requests.Session()
    s.headers.update({'User-Agent': usr_agent[random.randint(0, 4)],
                      'Host': 'www.xicidaili.com'})
    r = s.get('http://www.xicidaili.com/nn/1')
    soup = BeautifulSoup(r.content.decode(), "lxml")
    l = list(soup.find_all("tr"))[1:]
    cnt = 0
    for cell in l:
        tmp = cell.find_all("td")
        if 'fast' in tmp[6].div.div['class'] and "HTTPS" == tmp[5].text:
            ip = tmp[1].string
            port = tmp[2].string
            proxy = '{:s}:{:s}'.format(ip, port)
            if check_validation({"http": proxy}):
                cnt += 1
                yield proxy
        if cnt >= 5:
            break

if __name__ == '__main__':
    print(list(get_proxies()))
