import jieba.posseg
from ReadingAssistant.models import *
from .CentralEnt import *

def getCentralNode(condition):
	node = None
	words = jieba.possge.cut(condition)
	for word, tag in words:
		if tag == 'nr' or tag == 'nz':
			node = AuthorEnt(word)
			break
		elif tag in ['n', 'nd', 'ni', 'nl', 'ns', 'nt']:
			node = ImageEnt(word)
			break
		elif tag == 'a':
			node = EmotionEnt(word)
			break
	return node


def exactSearch(condition):
	result = Poem.objects.filter(poem_name=condition)
	if not result.exists():
		return None
	return PoemEnt(condition)


def search(condition):
	node = exactSearch(condition)
	if node is not None:
		return node
	node = getCentralNode(condition)
	return node

