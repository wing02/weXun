#coding=utf-8
import json
import re
import codecs

class Integra:
    def __init__(self,fileName):
        self.root=dict()
        f=open(fileName)
        for line in f:
            item=json.loads(line)
            title=item['title']
            if title in self.root:
                self.root[title].append(item)
            else:
                self.root[title]=[item]
        f.close()

    def allNews(self,integraType):
        #for title,items in self.root.iteritems():
        for title in self.root:
            items=self.root[title]
            length=len(items)
            if length==1:
                yield items[0]
            else:
                hasAll=False
                sortedItems=['']*(length)
                for item in items:
                    result=re.search('(\d*)\.[^/]*$',item['url'])
                    if result:
                        pageNum=result.group(1)
                        pageNum=int(pageNum)-1
                        if pageNum>length:
                            pageNum=0
                        sortedItems[pageNum]=item
                    else:
                        result=re.search('all\.[^/]*$',item['url'])
                        if result:
                            hasAll=True
                            break
                        else:
                            print 'Error Url:',item['url']
                if not hasAll:
                    content=''
                    images=[]
                    for item in sortedItems:
                        if item!='':
                            content+=item['contentWithImg']
                            images+=item['images']
                    if integraType=='oCaI':
                        sortedItems[0]['images']=images
                    elif integraType=='aCaI':
                        sortedItems[0]['contentWithImg']=content
                        sortedItems[0]['images']=images
                    yield sortedItems[0]
                else:
                    hasAll=False

    def writeFile(self,fileName,integraType):
        f = codecs.open(fileName,'wb',encoding='utf-8')
        for item in self.allNews(integraType):
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            f.write(line)
        f.close()


if __name__=="__main__":
    Integra('210102.json').writeFile('210102-2.json','oCaI')
