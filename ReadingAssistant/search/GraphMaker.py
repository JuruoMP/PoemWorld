# -*- coding:utf-8 -*-
class GraphMaker():
    def __init__(self):
        self.count = 0
        self.nodeList = []
        self.linkList = []
        #Change: the key of nodeDict is a string of "entType_entId".
        #Note that the "entId" refers to the primary key of entity in database,
        #all other "id" in code context refers to the index in the json list
        self.nodeDict = {}

    def getNodeIndex(self, priKey, entType):
        key = str(entType) + '_' + str(priKey)
        if self.nodeDict.get(key) is not None:
            return self.nodeDict[key]
        else:
            return -1


    def addNode(self, priKey, entName, entType):
        key = str(entType) + '_' + str(priKey)
        if self.nodeDict.get(key) is None:
            newNode = {}
            newNode['id'] = priKey
            newNode['name'] = entName#.encode('utf-8')
            newNode['type'] = entType
            self.nodeList.append(newNode)
            self.nodeDict[key] = self.count
            self.count = self.count + 1
        return self.nodeDict[key]

    def addNodeSet(self, qset):
        for record in qset:
            nodeType = record.entity_type

            if nodeType == "author":
                nodeId = record.author_id
                content = record.author_name
            elif nodeType == "poem":
                nodeId = record.poem_id
                content = record.poem_name
            elif nodeType == "image":
                nodeId = record.image_id
                content = record.image_name
            else:
                pass

            self.addNode(nodeId, content, nodeType)

    def addLink(self, srcNodeId, dstNodeId, typeName):
        newLink = {}
        newLink['source'] = srcNodeId
        newLink['target'] = dstNodeId
        newLink['value'] = typeName#.encode('utf-8')
        self.linkList.append(newLink)

    def toJson(self):
        jsonData = {}
        jsonData['nodes'] = self.nodeList
        jsonData['links'] = self.linkList
        return jsonData

