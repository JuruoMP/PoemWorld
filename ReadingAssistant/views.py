# -*- coding:utf-8 -*-
import json
from django.shortcuts import *
from django.http import HttpResponse
from .webcookie import *
import time
from .datas import *
from .generate import *

# Create your views here.


def map(request):
    return render_to_response("graph.html",
                              {"center_entity": "ALL",
                               "json": json})


def searchCondition(request, condition):
    return render_to_response("graph.html",
                              {"center_entity": condition,
                               "json": json})


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


def generate_poem(request):
    getPoem()
    cookie = getCookie('http://cts.388g.com/')
    print(cookie)
    #pgv_pvi = cookie['pgv_pvi']
    pgv_pvi = '9436215296'
    #pgv_si = cookie['pgv_si']
    pgv_si = 's3932924928'
    response = render(request, 'gen_poem.html')
    response.set_cookie('pgv_pvi', pgv_pvi)
    response.set_cookie('pgv_si', pgv_si)
    return response


def demo(request):
    return render_to_response('demo.html', {})


def test(request):
    return render_to_response('test.html', {})
