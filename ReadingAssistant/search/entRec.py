import jieba.posseg
from ReadingAssistant.models import *

def getEntList_bak(text):
	words = jieba.posseg.cut(text)
	entList = set([])
	for word, tag in words:
		if tag == 'nr' or tag == 'nz':
			try:
				record = Author.objects.get(author_name=word)
			except Exception:
				pass
			else:
				entList.add(word)
			try:
				record = Image.objects.get(image_name=word)
			except Exception:
				pass
			else:
				entList.add(word)
		elif tag in ['n', 'nd', 'ni', 'nl', 'ns', 'nt']:
			try:
				recSet = Image.objects.filter(image_name=word)
			except:
				pass
			else:
				if recSet.exists():
					entList.add(word)
	return entList

def getEntList(text, imageOnly=False):
	#tokens = jieba.tokenize(text, mode='search')
	tokens = jieba.tokenize(text)
	entList = set([])
	splitPoints = []
	for word in tokens:
		try:
			record = Author.objects.get(author_name=word[0])
		except Exception:
			pass
		else:
			if not imageOnly:
				entList.add(word[0])
				splitPoints.append((word[1], word[2]))

		try:
			recSet = Image.objects.filter(image_name=word[0])
		except Exception:
			pass
		else:
			if recSet.exists():
				entList.add(word[0])
				splitPoints.append((word[1], word[2]))
	#sorted(splitPoints, key=lambda point : point[0])
	return entList, splitPoints 

def addHref2Text(text):
	_, splitPoints = getEntList(text)
	entList = []
	contextList = []
	latestPt = 0
	for pTuple in splitPoints:
		entName = text[pTuple[0]:pTuple[1]]
		link = '/map/search/condition=' + entName
		entList.append('<a href="' + link + '">' + entName + '</a>')
		contextList.append(text[latestPt:pTuple[0]])
		latestPt = pTuple[1]
	content = ""
	for i in range(len(entList)):
		content = content + contextList[i] + entList[i]
	content = content + text[latestPt:-1]
	return content

		
		
		



