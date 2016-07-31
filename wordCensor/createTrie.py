#codeing=utf-8

import cPickle
import glob
from trie import Trie
import os.path as osp
import re
import pdb

senTypes=['politics','sexy','adv']
triePath='trie.pkl'
myTrie=Trie()

for senType in senTypes:
    paths=glob.glob(osp.join('dict',senType,'*'))
    for path in paths:
        f=open(path)
        for line in f:
            word=re.search('(.*)=',line).group(1).decode('u8')
            myTrie.insert(word,senType)
            #print word
        f.close()

f=open(triePath,'wb')
#pdb.set_trace()
#cPickle.dump(myTrie.root,f)
cPickle.dump(myTrie,f)
f.close()
