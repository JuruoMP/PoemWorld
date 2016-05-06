# -*- coding:utf-8 -*-
from ReadingAssistant.models import *
from math import log
class GraphMaker():
    def __init__(self, minSize=14, maxSize=24):
        self.count = 0
        self.minSize = minSize
        self.maxSize = maxSize
        self.nodeList = []
        self.linkList = []
        #Change: the key of nodeDict is a string of "entType_entId".
        #Note that the "entId" refers to the primary key of entity in database,
        #all other "id" in code context refers to the index in the json list
        self.nodeDict = {}
        self.linkDict = {}

    def getNodeIndex(self, priKey, entType):
        key = str(entType) + '_' + str(priKey)
        if self.nodeDict.get(key) is not None:
            return self.nodeDict[key]
        else:
            return -1

    def addNode(self, priKey, entName, entType, score=16, thumbPath=None, isCenter=False):
        key = str(entType) + '_' + str(priKey)
        if self.nodeDict.get(key) is None:
            newNode = {}
            newNode['id'] = priKey
            newNode['name'] = entName
            newNode['type'] = entType
            newNode['size'] = self.score2Size(score)

            if thumbPath is not None:
                circledThumbPath = thumbPath.split('.')
                thumbPath = circledThumbPath[0] + '_circle.' + circledThumbPath[1]
                newNode['thumb'] = thumbPath

            if isCenter:
                newNode['centered'] = 1
                newNode['size'] = 30
            else:
                newNode['centered'] = 0

            newNode['weight'] = newNode['size']
            
            self.nodeList.append(newNode)
            self.nodeDict[key] = self.count
            self.count = self.count + 1
        return self.nodeDict[key]

    def addNodeSet(self, qset):
        for record in qset:
            nodeType = record.entity_type
            thumbPath = None

            if nodeType == "author":
                nodeId = record.author_id
                content = record.author_name
                thumb_temp = record.author_head_thumb
                score = 8
                if len(thumb_temp) != 0:
                    thumbPath = thumb_temp
            elif nodeType == "poem":
                nodeId = record.poem_id
                content = record.poem_name
                score = record.poem_score
            elif nodeType == "image":
                nodeId = record.image_id
                content = record.image_name
                score = 8
            else:
                pass

            self.addNode(nodeId, content, nodeType, score=score, thumbPath=thumbPath)

    def addLink(self, srcNodeId, dstNodeId, typeName):
        newLink = {}
        if self.linkDict.get(str(srcNodeId) + '_' + str(dstNodeId)) is None:
            newLink['source'] = srcNodeId
            newLink['target'] = dstNodeId
            newLink['value'] = typeName
            self.linkList.append(newLink)
            self.linkDict[str(srcNodeId) + '_' + str(dstNodeId)] = True

    def toJson(self):
        jsonData = {}
        jsonData['nodes'] = self.nodeList
        jsonData['links'] = self.linkList
        return jsonData

    def score2Size(self, score):
        factor = (self.maxSize - self.minSize) / (log(29) - log(1))
        #factor = (self.maxSize - self.minSize) / (29 - 1)
        return int(log(score) * factor + self.minSize)
        #return int(score) * factor + self.minSize)


