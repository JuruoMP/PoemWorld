import jieba.posseg
jieba.load_userdict("imagedict.txt")
from ReadingAssistant.models import *
from ReadingAssistant.search.entRec import *
def preRenderAuthors(startIndex, endIndex):
	for aid in range(startIndex, endIndex):
		qset = Author.objects.filter(author_id=aid)
		record = qset[0]
		if len(record.author_desc) != 0:
			renderDesc = '<p>' + addHref2Text(record.author_desc).replace('\\n\\r', '</p><p>').replace('\\r\\n', '</p><p>')\
						.replace('\\n', '</p><p>').replace('\\r', '</p><p>') + '</p>'
			qset.update(author_desc_after_render=renderDesc)


def preRenderPoems(startIndex, endIndex):
	for pid in range(startIndex, endIndex):
		if pid % 25 == 0:
			print("processing 25....")
		qset = Poem.objects.filter(poem_id=pid)
		record = qset[0]
		renderContent = '<p>' + addHref2Text(record.poem_content).replace('\\n\\r', '</p><p>').replace('\\r\\n', '</p><p>')\
						.replace('\\n', '</p><p>').replace('\\r', '</p><p>') + '</p>'
		qset.update(poem_content_after_render=renderContent)
		if len(record.poem_analysis) != 0:
			renderAnalysis = '<p>' + addHref2Text(record.poem_analysis).replace('\\n\\r', '</p><p>').replace('\\r\\n', '</p><p>')\
										.replace('\\n', '</p><p>').replace('\\r', '</p><p>') + '</p>'
			qset.update(poem_analysis_after_render=renderAnalysis)