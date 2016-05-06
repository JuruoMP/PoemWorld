import re
from .pinyin import pinyin

def analysis_yunlv(lines):
    try:
        content = ''
        for line in lines:
            content = content + line.replace('\n', '')
        content = re.split('。|！|？', content)
        contents = []
        for c in content:
            if c != '':
                contents.append(c)
        sounds = []
        for content in contents:
            word = content[-1]
            #print(pinyin[word])
            if pinyin[word][-1] == 'g':
                #print(pinyin[word][-3:])
                sounds.append(pinyin[word][-3:])
            else:
                sounds.append(pinyin[word][-1])
        result = ''
        correct = sounds[0]
        judge = True
        for sound in sounds:
            result += sound + '；'
            if sound != correct:
                judge = False
        yunlv_result = {}
        yunlv_result['yunlv_sound'] = result
        if judge == True:
            yunlv_result['yunlv_judge'] = '符合韵律'
        else:
            yunlv_result['yunlv_judge'] = '不符合韵律'
        return yunlv_result
    except:
        return {}
'''
if __name__ == '__main__':
    file = open('test.txt', 'r')
    lines = file.readlines()
    yunlv_result = analysis_yunlv(lines)
    print(yunlv_result)
'''
