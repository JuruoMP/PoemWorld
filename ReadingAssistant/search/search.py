import jieba.posseg
from ReadingAssistant.models import *
from .CentralEnt import *
from .GraphMaker import *


def getCentralEnt(condition):
    node = None
    words = jieba.posseg.cut(condition)
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

#This function will find the central node(a CentralEnt object) in the graph
def search4CNode(condition):
    node = exactSearch(condition)
    if node is not None:
        return node
    node = getCentralEnt(condition)
    return node
