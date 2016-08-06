#coding=utf-8
from __future__ import (division,absolute_import,print_function,unicode_literals,)
#from builtins import *
#from future.builtins.disabled import *
#from future.utils import with_metaclass

from trie import Trie

trie=Trie()
s1=u'日本'
s2=u'日本男人'
s3=u'日本女人'
s4=u'日本男'
s5=u'日本男人2'

trie.insert(s1,1)
#trie.insert(s2,1)

string=u'和日本友好相处'
for i in range(len(string)):
    print (trie.find(string,i))
#print trie.find(s1)
#print trie.find(s2)
#print trie.find(s3)
#print trie.find(s4)
#print trie.find(s5)
