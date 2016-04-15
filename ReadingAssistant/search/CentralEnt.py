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
        nodeType = self.record.entity_type
        thumbPath = None
        if nodeType == "author":
            priKey = self.record.author_id
            thumb_temp = self.record.author_head_thumb
            if len(thumb_temp) != 0:
                thumbPath = thumb_temp
        elif nodeType == "poem":
            priKey = self.record.poem_id
        elif nodeType == "image":
            priKey = self.record.image_id
        else:
            priKey = self.record.emotion_desc
        self.nodeId = graphMaker.addNode(priKey, self.content, nodeType, thumbPath)
        return self.nodeId

    #This function will return a QuerySet of candidate central entities
    def executeQuery(self):
        pass

    def extendRels(self, graphMaker):
        pass



class AuthorEnt(CentralEnt):
    def __init__(self, content, record=None):
        CentralEnt.__init__(self, content, record)

    def executeQuery(self):
        qset = Author.objects.filter(author_name=self.content)
        if not qset.exists():
            return False
        self.record = qset[0]
        self.content = self.record.author_name
        return True

    def extendRels(self, graphMaker):
        newNodes = []
        relset1 = Author_Poem.objects.filter(author=self.record.author_id)
        for rel in relset1:
            poem = rel.poem
            node = PoemEnt(poem.poem_name, poem)
            dstNodeId = node.addNode2Graph(graphMaker)
            newNodes.append(node)
            graphMaker.addLink(self.nodeId, dstNodeId, u"撰写")
        relset2 = Author_Poem.objects.filter(author=self.record.author_id)
        for rel in relset2:
            poem = rel.poem
            node = PoemEnt(poem.poem_name, poem)
            dstNodeId = node.addNode2Graph(graphMaker)
            newNodes.append(node)
            graphMaker.addLink(self.nodeId, dstNodeId, u"撰写")
        return newNodes


class PoemEnt(CentralEnt):
    def __init__(self, content, record=None):
        CentralEnt.__init__(self, content, record)

    def executeQuery(self):
        qset = Poem.objects.filter(poem_name__contains=self.content)
        if not qset.exists():
            return False
        self.record = qset[0]
        self.content = self.record.poem_name
        return True

    def extendRels(self, graphMaker):
        newNodes = []
        relset1 = Author_Poem.objects.filter(poem=self.record.poem_id)
        for rel in relset1:
            author = rel.author
            node = AuthorEnt(author.author_name, author)
            dstNodeId = node.addNode2Graph(graphMaker)
            newNodes.append(node)
            graphMaker.addLink(self.nodeId, dstNodeId, u"撰写")

        relset2 = Poem_Image.objects.filter(poem=self.record.poem_id)
        for rel in relset2:
            image = rel.image
            node = ImageEnt(image.image_name, image)
            dstNodeId = node.addNode2Graph(graphMaker)
            newNodes.append(node)
            graphMaker.addLink(self.nodeId, dstNodeId, u"使用意象")
        return newNodes

class ImageEnt(CentralEnt):
    def __init__(self, content, record=None):
        CentralEnt.__init__(self, content, record)

    def executeQuery(self):
        qset = Image.objects.filter(image_name__contains=self.content)
        if not qset.exists():
            return False
        self.record = qset[0]
        self.content = self.record.image_name
        return True

    def extendRels(self, graphMaker):
        newNodes = []
        relset1 = Poem_Image.objects.filter(image=self.record.image_id)
        for rel in relset1:
            poem = rel.poem
            node = PoemEnt(poem.poem_name, poem)
            dstNodeId = node.addNode2Graph(graphMaker)
            newNodes.append(node)
            graphMaker.addLink(self.nodeId, dstNodeId, u"相关诗歌")
        '''
        relset2 = Image_Emotion.objects.filter(image=self.record.image_id)
        for rel in relset2:
            emotion = rel.emotion
            node = EmotionEnt(emotion.emotion_name, emotion)
            dstNodeId =  node.addNode2Graph(graphMaker)
            newNodes.append(node)
            graphMaker.addLink(self.nodeId, dstNodeId, u"情感倾向")
        '''
        return newNodes