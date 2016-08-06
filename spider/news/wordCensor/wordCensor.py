#coding=utf-8
import glob
import os.path as osp
import re
import cPickle
class Trie:
    def __init__(self):
        self.root = dict()

    def insert(self, string,senType):
        index, node = self.findLastNode(string)
        for char in string[index:]:
            new_node = dict()
            node[char] = new_node
            node = new_node
        node['type']=senType

    def find(self,string,start):
        node=self.root
        for index in range(start,len(string)):
            char=string[index]
            if char in node:
                if 'type' in node[char]:
                    return (string[start:index+1],node[char]['type'])
                node=node[char]
            else:
                return None

    def findLastNode(self, string):
        '''
        @param string: string to be searched
        @return: (index, node).
            index: int. first char(string[index]) of string not found in Trie tree. Otherwise, the length of string
            node: dict. node doesn't have string[index].
        '''
        node = self.root
        index = 0
        while index < len(string):
            char = string[index]
            if char in node:
                node = node[char]
            else:
                break
            index += 1
        return (index, node)

    def printTree(self, node, layer):
        if len(node) == 0:
            return '\n'

        rtns = []
        items = sorted(node.items(), key=lambda x:x[0])
        rtns.append(items[0][0])
        rtns.append(self.printTree(items[0][1], layer+1))

        for item in items[1:]:
            rtns.append('.' * layer)
            rtns.append(item[0])
            rtns.append(self.printTree(item[1], layer+1))

        return ''.join(rtns)

    def __str__(self):
        return self.printTree(self.root, 0)

    @classmethod
    def loadTrie(cls,triePath):
        return cPickle.load(open(triePath))

    def hasSensi(self,content):
        for i in range(len(content)):
            result=self.find(content,i)
            if result:
                return result
        
    def saveTrie(self,triePath):
        f=open(triePath,'wb')
        cPickle.dump(self,f)
        f.close()


    def createTrie(self):
        senTypes=['politics','sexy','adv']
        for senType in senTypes:
            paths=glob.glob(osp.join('sensiDict',senType,'*'))
            for path in paths:
                f=open(path)
                for line in f:
                    word=re.search('(.*)=',line).group(1).decode('u8')
                    self.insert(word,senType)
                    print word
                f.close()


if __name__=="__main__":
    trie=Trie()
    trie.createTrie()
    triePath='sensitive.pkl'
    trie.saveTrie(triePath)

    newTrie=Trie.loadTrie(triePath)
    content=u'我人有的河中办发主场不为主'
    result= newTrie.hasSensi(content)
    if result:
        print result[0]
