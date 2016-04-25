# -*- coding:utf-8 -*-
from ReadingAssistant.models import *
from .GraphMaker import *
from django.db.models import Q

class CentralEnt:
    def __init__(self, content, record):
        self.nodeId = -1
        self.content = content
        self.record = record

    def getContent(self):
        return self.content

    def addNode2Graph(self, graphMaker, centerFlag=False):
        pass

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

    def addNode2Graph(self, graphMaker, centerFlag=False):
        priKey = self.record.author_id
        thumb_temp = self.record.author_head_thumb
        if len(thumb_temp) != 0:
            thumbPath = thumb_temp
        else:
            thumbPath = None
        self.nodeId = graphMaker.addNode(priKey, self.content, "author", score=8, thumbPath=thumbPath, isCenter=centerFlag)
        return self.nodeId

    def extendRels(self, graphMaker):
        newNodes = []
        relset1 = Author_Poem.objects.filter(author=self.record.author_id)
        for rel in relset1:
            poem = rel.poem
            node = PoemEnt(poem.poem_name, poem)
            dstNodeId = node.addNode2Graph(graphMaker)
            newNodes.append(node)
            graphMaker.addLink(self.nodeId, dstNodeId, u"撰写")
        relset2 = AuthorRelation.objects.filter(Q(author1=self.record.author_id) | Q(author2=self.record.author_id))
        for rel in relset2:
            if rel.author1.author_id == self.record.author_id:
                anotherId = rel.author2.author_id
            else:
                anotherId = rel.author1.author_id
            desc = rel.rel_desc
            try:
                anotherRecord = Author.objects.get(author_id=anotherId)
            except:
                continue
            else:
                node = AuthorEnt(anotherRecord.author_name, anotherRecord)
                dstNodeId = node.addNode2Graph(graphMaker)
                newNodes.append(node)
                graphMaker.addLink(self.nodeId, dstNodeId, desc)
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

    def addNode2Graph(self, graphMaker, centerFlag=False):
        priKey = self.record.poem_id
        self.nodeId = graphMaker.addNode(priKey, self.content, "poem", score=self.record.poem_score, isCenter=centerFlag)
        return self.nodeId

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

    def addNode2Graph(self, graphMaker, centerFlag=False):
        priKey = self.record.image_id
        self.nodeId = graphMaker.addNode(priKey, self.content, "image", score=3, isCenter=centerFlag)
        return self.nodeId

    def extendRels(self, graphMaker):
        newNodes = []
        relset1 = Poem_Image.objects.filter(image=self.record.image_id)
        for rel in relset1:
            poem = rel.poem
            node = PoemEnt(poem.poem_name, poem)
            dstNodeId = node.addNode2Graph(graphMaker)
            newNodes.append(node)
            graphMaker.addLink(self.nodeId, dstNodeId, u"相关诗歌")
        return newNodes