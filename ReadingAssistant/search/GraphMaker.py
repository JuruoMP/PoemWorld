# -*- coding:utf-8 -*-
class GraphMaker():
	def __init__(self):
		self.count = 0
		self.nodeList = []
		self.linkList = []
		self.nodeDict = {}
		

	def addNode(self, name, atype):
		if self.nodeDict.get(name) is None:
			newNode = {}
			newNode['name'] = name
			newNode['type'] = atype
			self.nodeList.append(newNode)
			self.nodeDict[name] = self.count
			self.count = self.count + 1
		return self.nodeDict[name]

	def addLink(self, srcNodeId, dstNodeId, typeName):
		newLink = {}
		newLink['source'] = srcNodeId
		newLink['target'] = dstNodeId
		newLink['value'] = typeName
		self.linkList.append(newLink)

	def toJson(self):
		jsonData = {}
		jsonData['nodes'] = self.nodeList
		jsonData['links'] = self.linkList
		return jsonData		

