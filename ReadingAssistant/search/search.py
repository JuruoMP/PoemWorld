# -*- coding:utf-8 -*-
import jieba.posseg
from ReadingAssistant.models import *
from .CentralEnt import *
from .GraphMaker import *


def getCentralEnt(condition):
    node = None
    words = jieba.posseg.cut(condition)
    for word, tag in words:
        if tag == 'nr' or tag == 'nz':
            node = AuthorEnt(word)
            break
        elif tag in ['n', 'nd', 'ni', 'nl', 'ns', 'nt']:
            node = ImageEnt(word)
            break
        '''
        elif tag == 'a':
            node = EmotionEnt(word)
            break
        '''
    return node


def exactSearch(condition):
    result = Poem.objects.filter(poem_name=condition)
    if result.exists():
        return PoemEnt(condition)
    result = Author.objects.filter(author_name=condition)
    if result.exists():
        return AuthorEnt(condition)
    result = Image.objects.filter(image_name=condition)
    if result.exists():
        return ImageEnt(condition)
    '''
    result = Emotion.objects.filter(emotion_desc=condition)
    if result.exists():
        return EmotionEnt(condition)
    '''
    return None

#This function will find the central node(a CentralEnt object) in the graph
def search4CNode(condition):
    node = exactSearch(condition)
    if node is not None:
        return node
    node = getCentralEnt(condition)
    return node

def getWholeGraph():
    graphMaker = GraphMaker()
    aRecords = Author.objects.all()
    graphMaker.addNodeSet(aRecords)
    pRecords = Poem.objects.all()
    graphMaker.addNodeSet(pRecords)
    iRecords = Image.objects.all()
    graphMaker.addNodeSet(iRecords)
    '''
    eRecords = Emotion.objects.all()
    graphMaker.addNodeSet(eRecords)
    '''

    a_pLinks = Author_Poem.objects.all()
    for link in a_pLinks:
        aid = graphMaker.getNodeIndex(link.author_id, "author")
        pid = graphMaker.getNodeIndex(link.poem_id, "poem")
        graphMaker.addLink(aid, pid, u"撰写")

    p_iLinks = Poem_Image.objects.all()
    for link in p_iLinks:
        pid = graphMaker.getNodeIndex(link.poem_id, "poem")
        iid = graphMaker.getNodeIndex(link.image_id, "image")
        graphMaker.addLink(pid, iid, u"使用意象")

    '''
    i_eLinks = Image_Emotion.objects.all()
    for link in i_eLinks:
        iid = graphMaker.getNodeIndex(link.image_id, "image")
        eid = graphMaker.getNodeIndex(link.emotion_id, "emotion")
        graphMaker.addLink(iid, eid, u"情感倾向")
    '''

    return graphMaker