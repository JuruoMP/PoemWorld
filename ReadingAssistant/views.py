# -*- coding:utf-8 -*-
import json
from django.shortcuts import *
from django.http import HttpResponse
from .webcookie import *
import time
from .generate import *
from ReadingAssistant.search.search import *

# Create your views here.


def homePage(request):
    return render_to_response('homepage.html')


def map(request):
    graphMaker = getWholeGraph()
    print(graphMaker)
    return render_to_response("graph.html",
                              {"center_entity": "ALL",
                               "json": graphMaker.toJson()})


def searchCondition(request, condition):
    cNode = search4CNode(condition)
    if len(condition) == 0:
        graphMaker = getWholeGraph()
        return render_to_response("graph.html",
                                  {"center_entity": "ALL",
                                   "json": graphMaker.toJson()})
    if cNode is None or not cNode.executeQuery():
        return render_to_response("graph.html",
                                  {"center_entity": "None", })
    graphMaker = GraphMaker()
    cNode.addNode2Graph(graphMaker, centerFlag=True)
    adjNodes = cNode.extendRels(graphMaker)
    for aNode in adjNodes:
        if not isinstance(aNode, ImageEnt) and not isinstance(aNode, AuthorEnt):
            aNode.extendRels(graphMaker)
    #print graphMaker.toJson()
    return render_to_response("graph.html",
                              {"center_entity": cNode.getContent(),
                               "json": graphMaker.toJson()})


def hello(request):
    visit_time = time.strftime('%H:%M:%S')
    return render_to_response('hello.html',
                              {'visit_time': visit_time})


def entity_modal(request):
    type = request.GET['type']
    entId = request.GET['entId']
    renderDict = {}
    try:
        eid = int(entId)
    except Exception:
        pass
    else:
        if type == 'author':
            try:
                record = Author.objects.get(author_id=entId)
            except Author.DoesNotExist:
                pass
            else:
                renderDict['entity_name'] = record.author_name
                renderDict['author_name'] = record.author_name
                renderDict['entity_type'] = 'author'
                if len(record.author_head_thumb) != 0:
                    renderDict['author_head_thumb'] = record.author_head_thumb
                if len(record.author_belong) != 0:
                    renderDict['author_belong'] = record.author_belong
                if len(record.author_birth) != 0 and len(record.author_death) != 0:
                    renderDict['author_birth'] = record.author_birth
                    renderDict['author_death'] = record.author_death
                if len(record.author_desc) != 0:
                    renderDict['author_desc'] = '<p>' + record.author_desc.replace('\\n\\r', '</p><p>').replace('\\r\\n', '</p><p>')\
                        .replace('\\n', '</p><p>').replace('\\r', '</p><p>') + '</p>'
        elif type == 'poem':
            try:
                record = Poem.objects.get(poem_id=entId)
            except Poem.DoesNotExist:
                pass
            else:
                renderDict['entity_name'] = record.poem_name
                renderDict['poem_name'] = record.poem_name
                renderDict['entity_type'] = 'poem'
                # TODO: make href to entities on poem
                renderDict['poem_content'] = '<p>' + record.poem_content.replace('\\n\\r', '</p><p>').replace('\\r\\n', '</p><p>')\
                    .replace('\\n', '</p><p>').replace('\\r', '</p><p>') + '</p>'
                if len(record.poem_year) != 0:
                    renderDict['poem_year'] = record.poem_year
                if len(record.poem_kind) != 0:
                    renderDict['poem_kind'] = record.poem_kind
                if len(record.poem_pinyin) != 0:
                    renderDict['poem_pinyin'] = record.poem_pinyin
                if len(record.poem_analysis) != 0:
                    renderDict['poem_analysis'] = '<p>' + record.poem_analysis.replace('\\n\\r', '</p><p>').replace('\\r\\n', '</p><p>')\
                        .replace('\\n', '</p><p>').replace('\\r', '</p><p>') + '</p>'
                renderDict['poem_audio'] = '/static/audio/demo.mp3'
        elif type == 'image':
            try:
                record = Image.objects.get(image_id=entId)
            except Image.DoesNotExist:
                pass
            else:
                renderDict['entity_name'] = record.image_name
                renderDict['image_name'] = record.image_name
                renderDict['entity_type'] = 'image'
                relset1 = Image_Emotion.objects.filter(image=record.image_id)
                emotionList = []
                eStrList = []
                for rel in relset1:
                    emotion = rel.emotion
                    emotionList.append(emotion)
                    eStrList.append(emotion.emotion_desc)
                renderDict['image_emotion'] = ' '.join(eStrList)
                iStrList = []
                for emotion in emotionList:
                    relset2 = Image_Emotion.objects.exclude(image=record.image_id).filter(emotion=emotion.emotion_id)
                    for rel in relset2:
                        image_name = rel.image.image_name
                        link = '/map/search/condition=' + image_name
                        content = '<a href="' + link + '">' + image_name + '</a>'
                        # iStrList.append(rel.image.image_name)
                        iStrList.append(content)
                renderDict['images'] = iStrList
        else:
            pass
    return render_to_response('modal.html', renderDict)


def generate_poem_empty(request):
    return render_to_response('gen_poem.html', {})


def generate_poem(request, string, num, type, yayuntype):
    content = getPoem(string, num, type, yayuntype)
    return render_to_response('gen_poem.html',
                              {'generated': 'true',
                               'generate_response': content})


def analysis_empty(request):
    return render_to_response('analysis.html')


def analysis(request):
    content = request.GET['content']
    result = '12345678'
    return render_to_response('analysis_result.html',
                              {'analysis_result': result})


def rank_model(request):
    return render_to_response('rank_model.html', {})


def demo(request):
    return render_to_response('demo.html', {})


def test(request):
    return render_to_response('test.html', {})
