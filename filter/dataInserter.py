#coding=utf8
import sys
import os.path as osp
import MySQLdb
import pytfs
import glob

class DataInserter:
    def __init__(self,updateTime):
        self.filters=[]
        self.dbIp='localhost'
        self.dbUser='wexun'
        self.dbPasswd='wexun'
        self.dbName='wexun'
        self.update_time=''
        self.tfsUrl='10.198.19.176:8100'
        self.dataPrePath=''
        self.tfsPrePath='http://10.198.19.176:8080/v1/tfs/'
        self.updateTime=updateTime

        self.db = MySQLdb.connect(self.dbIp,self.dbUser,self.dbPasswd,self.dbName, charset='utf8')
        self.cursor = self.db.cursor()
        self.tfs = pytfs.TfsClient()
        self.tfs.tfs_init(self.tfsUrl)

    def __del__(self):
        db.close()

    def insertFromRexpath(rexpath):
        for path in glob.glob(rexpath):
            self.insertFromFile(path)

    def insertFromFile(filePath):
        f=open(filePath)
        for line in f:
            item=json.loads(line)
            insertFromJson(item)
        f.close()

    def insertFromJson(jsItem):
        images=jsItem['images']
        imageTfsNames=[]
        subImageTfsNames=[]
        item=dict()

        for image in images:
            path=self.dataPrePath+image['path']
            with open(path) as f:
                imageTfsNames.append(self.tfs.put(f.read()))
        content=jsItem['contentWithImg']
        content='<p>'+re.sub('{up}','</p><p>',content)+'</p>'
        for imageTfsName in imageTfsNames:
            src=self.tfsPrePath+imageTfsName
            content=re.sub('{img}','<img src="'+src+'">',content,1)
        content=re.sub('{img}','',content)
        item['news_data']=self.tfs.put(content)

        for i,image in enumerate(images):
            if i=3:
                break
            path=self.dataPrePath+re.sub('full','thumbs/small',image['path'])
            with open(path) as f:
                subImageTfsNames.append(self.tfs.put(f.read()))
        item['news_imgs']=','.join(subImageTfsNames)
        item['news_title']=jsItem['title'][:33]
        item['news_resource_link']=re.search('[^?]*',jsItem['url']).group()
        item['news_time']=jsItem['time']
        item['update_time']=self.updateTime
        item['agency_name']=jsItem['spider']
        item['flag']='unknown'
        item['news_abstract']=re.sub('{up}|{img}','',jsItem['contentWithImg'])[:80]
        item['news_type']='new'

        sql=''' INSERT INTO news(%s) VALUES('%s')'''%(','.join(item.keys()) ,"','".join(item.values() ) )
        sql=sql.encode('u8')
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error,e:
            self.db.rollback()
            print "MySQL Error:%s"%str(e)
            print sql

if __name__=="__main__":
    update_time='20160818112230'
    dataInserter=DataInserter(update_time)
    dataInserter.insertFromRexpath('')
