# -*- coding:utf-8 -*-
from ReadingAssistant.models import *
from .GraphMaker import *

class CentralEnt:
	def __init__(self, content, record):
		self.nodeId = -1
		self.content = content
		self.record = record

	def getContent(self):
		return self.content

	def addNode2Graph(self, graphMaker):
		self.NodeId = graphMaker.addNode(content)

	#This function will return a QuerySet of candidate central entities
	def executeQuery(self):
		pass

	def extendRels(self, graphMaker):
		pass



class AuthorEnt(CentralEnt):
	def __init__(self, content, record=None):
		CentralEnt.__init__(self, content, record)

	def executeQuery(self):
		qset = Author.objects.filter(author_name=content)
		if not qset.exists():
			return False
		self.record = qset[0]
		self.content = self.record.author_name
		return True

	def extendRels(self, graphMaker):
		newNodes = []
		relset = Author_Poem.objects.filter(author_id=self.record.author_id)
		for rel in relset:
			poem = rel.poem_id
			node = PoemEnt(poem.poem_name, poem)
			newNodes.append(node)
			graphMaker.addLink(nodeId, poem.poem_name, u"撰写")
		return newNodes


class PoemEnt(CentralEnt):
	def __init__(self, content, record=None):
		CentralEnt.__init__(self, content, record)

	def executeQuery(self):
		qset = Poem.objects.filter(poem_name__contains=content)
		if not qset.exists():
			return False
		self.record = qset[0]
		self.content = self.record.poem_name
		return True

	def extendRels(self, graphMaker):
		newNodes = []
		relset1 = Author_Poem.objects.filter(poem_id=self.record.poem_id)
		for rel in relset1:
			author = rel.author_id
			node = AuthorEnt(author.author_name, author)
			newNodes.append(node)
			graphMaker.addLink(nodeId, author.author_name, u"撰写")

		relset2 = Poem_Image.objects.filter(poem_id=self.record.poem_id)
		for rel in relset2:
			image = rel.image_id
			node = ImageEnt(image.image_name, image)
			newNodes.append(node)
			graphMaker.addLink(nodeId, image.image_name, u"使用意象")
		return newNodes

class ImageEnt(CentralEnt):
	def __init__(self, content, record=None):
		CentralEnt.__init__(self, content, record)

	def executeQuery(self):
		qset = Image.objects.filter(image_name__contains=content)
		if not qset.exists():
			return False
		self.record = qset[0]
		self.content = self.record.image_name
		return True

	def extendRels(self, graphMaker):
		newNodes = []
		relset1 = Poem_Image.objects.filter(image_id=self.record.image_id)
		for rel in relset1:
			poem = rel.poem_id
			node = PoemEnt(poem.poem_name, poem)
			newNodes.append(node)
			graphMaker.addLink(nodeId, poem.poem_name, u"相关诗歌")
				
		relset2 = Image_Emotion.objects.filter(image_id=self.record.image_id)
		for rel in relset2:
			emotion = rel.emotion_id
			node = EmotionEnt(emotion.emotion_name, emotion)
			newNodes.append(node)
			graphMaker.addLink(nodeId, emotion.emotion_name, u"情感倾向")
		return newNodes

class EmotionEnt(CentralEnt):
	def __init__(self, content, record=None):
		CentralEnt.__init__(self, content, record)

	def executeQuery(self):
		qset = Emotion.objects.filter(emotion_desc__contains=content)
		if not qset.exists():
			return False
		self.record = qset[0]
		self.content = self.record.emotion_desc
		return True

	def extendRels(self, graphMaker):
		newNodes = []
		relset = Image_Emotion.objects.filter(emotion_id=self.record.emotion_id)
		for rel in relset:
			image = rel.image_id
			node = ImageEnt(image.image_name, image)
			newNodes.append(node)
			graphMaker.addLink(nodeId, image.image_name, u"情感倾向")
		return newNodes