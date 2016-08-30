import matplotlib.pyplot as plt
import cPickle


goodPkl='scores2.pkl'
#badPkl='scores2.pkl'
goods=cPickle.load(open(goodPkl))
#bads=cPickle.load(open(badPkl))

goodList=[0]*100
i=0
for good in goods:
    score=int(good*100)
    goodList[score]+=1
    i+=1
    if i>len(goods)/10:
        break

plt.bar(range(len(goodList)),goodList,color = 'red')
#plt.plot(range(len(good)),good,'b*')
#plt.plot(range(len(bad)),bad,'r*')
plt.show()
