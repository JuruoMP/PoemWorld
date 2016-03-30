import urllib.request
import urllib.response
import urllib.parse
import http.cookiejar
import re

def getPoem():
    url = 'http://cts.388g.com/'
    webpage = urllib.request.urlopen(url)
    content = webpage.read().decode('gb2312')

