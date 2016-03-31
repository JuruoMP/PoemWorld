import urllib.request
import urllib.response
import urllib.parse
import http.cookiejar
import re
from django import forms

def getPoem(string, num, type, yayuntype):
    url = 'http://cts.388g.com/'
    webpage = urllib.request.urlopen(url)
    content = webpage.read().decode('gb2312')
    #print(content)
    #string = '一花一世界'
    string = string
    str_utf8 = ''
    for item in string:
        str_utf8 += '%u' + '%x' % ord(item)
    #str_utf8 = '%u6211%u81EA%u503E%u6000%u541B%u4E14%u968F%u610F'
    url = 'http://cts.388g.com/fasong.php?w=' + str_utf8 + '&num=' + num + '&type=' + type + '&yayuntype=' + yayuntype
    webpage = urllib.request.urlopen(url)
    content = webpage.read().decode('gbk')
    #print(content)
    return content

