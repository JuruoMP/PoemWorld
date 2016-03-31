# -*- coding:utf-8 -*-
import json
from django.shortcuts import *
from django.http import HttpResponse
from .webcookie import *
import time
from .datas import *
from .generate import *
from .search.search imort *


# Create your views here.


def map(request):
    return render_to_response("graph.html",
                              {"center_entity": "ALL",
                               "json": json})


def searchCondition(request, condition):
    cNode = search(condition)
    if cNode is None or not cNode.executeQuery():
        #How to handle this branch?
        pass
    graphMaker = GraphMaker()
    cNode.addNode2Graph(graphMaker)
    AdjNodes = extendRels(graphMaker)
    for aNode in AdjNodes:
        aNode.extendRels(graphMaker)
    return render_to_response("graph.html",
                              {"center_entity": cNode.getContent(),
                               "json": graphMaker.toJson()})


def hello(request):
    visit_time = time.strftime('%H:%M:%S')
    return render_to_response('hello.html',
                              {'visit_time': visit_time})


def entity_modal(request, entity):
    return render_to_response('modal.html',
                              {'entity': entity,
                               'image_url': 'https://github.com/favicon.ico',
                               'entity_name': 'ENTITY_NAME',
                               'entity_info': 'ENTITY_INFO'})


def generate_poem_empty(request):
    return render_to_response('gen_poem.html', {})

def generate_poem(request, string, num, type, yayuntype):
    content = getPoem(string, num, type, yayuntype)
    return render_to_response('gen_poem.html',
                              {'generated': 'true',
                               'generate_response': content})


def demo(request):
    return render_to_response('demo.html', {})


def test(request):
    return render_to_response('test.html', {})