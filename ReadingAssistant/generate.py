import urllib.request
import urllib.response
import urllib.parse
import http.cookiejar
import re
from django import forms

default = '<div class=\"ui centered cards\"><div class=\"ui card\"><div id=\'commetcontentNew\'><font color=red><b>冯</b></font>夷矜海若，<br/><font color=red><b>如</b></font>今花正多。<br/><font color=red><b>杯</b></font>接近臣欢，<br/><font color=red><b>好</b></font>日当秋半。<br/></div></div><div class=\"ui card\"><div id=\'commetcontentNew1\'><font color=red><b>冯</b></font>翊蒲西郡，<br/><font color=red><b>如</b></font>公尽雄俊。<br/><font color=red><b>杯</b></font>中忽复醉，<br/><font color=red><b>好</b></font>是潺湲水。<br/></div></div><div class=\"ui card\"> <div id=\'commetcontentNew2\'><font color=red><b>冯</b></font>生远同恨，<br/><font color=red><b>如</b></font>有肤受谮。<br/><font color=red><b>杯</b></font>酒逢花住，<br/><font color=red><b>好</b></font>音怜铩羽。<br/></div></div><div class=\"ui card\"><div id=\'commetcontentNew3\'><font color=red><b>冯</b></font>谖愧有鱼，<br/><font color=red><b>如</b></font>何悲此曲。<br/><font color=red><b>杯</b></font>浮紫菊花，<br/><font color=red><b>好</b></font>就松阴挂。<br/></div></div><div class=\"ui card\"> <div id=\'commetcontentNew4\'><font color=red><b>冯</b></font>公尚戢翼，<br/><font color=red><b>如</b></font>何属秋气。<br/><font color=red><b>杯</b></font>酒沾津吏，<br/><font color=red><b>好</b></font>视忽生疵。<br/></div></div><div class=\"ui card\"> <div id=\'commetcontentNew5\'><font color=red><b>冯</b></font>异献赤伏，<br/><font color=red><b>如</b></font>天落镜湖。<br/><font color=red><b>杯</b></font>来秋兴高，<br/><font color=red><b>好</b></font>勇知名早。<br/></div></div></div>'

def getPoem(string, num, type, yayuntype):
    if string == '冯如杯好' and num == '5' and type == '1' and yayuntype == '1':
        return default
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
    content = content.replace('<ul>', '<div class="ui centered cards">').replace('</ul>', '</div>')
    content = content.replace('<li>', '<div class="ui card">').replace('</li>', '</div>')
    #print(content)
    return content
