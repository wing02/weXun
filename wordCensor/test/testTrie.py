#coding=utf-8

from trie import Trie

trie=Trie()
s1=u'日本'
s2=u'日本男人'
s3=u'日本女人'
s4=u'日本男'
s5=u'日本男人2'

trie.insert(s2,1)
trie.insert(s3,1)

print trie.find(s1)
print trie.find(s2)
print trie.find(s3)
print trie.find(s4)
print trie.find(s5)
