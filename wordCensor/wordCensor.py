
import jieba
import cPickle

class WordCensor:
    def __init__(self):
        triePath=''
        self.trie=cPickle.load(open(triePath))

    def hasSensi(self,content):
        words=jieba.cut(content.decode('u8'),cut_all=True)
        for word in words:
            result=self.trie.find(word)
            if result:
                return result
