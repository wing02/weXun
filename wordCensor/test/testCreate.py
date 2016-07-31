#coding=utf-8
import cPickle

triePath='trie.pkl'
trie=cPickle.load(open(triePath))
print trie.find(u'满狗')
