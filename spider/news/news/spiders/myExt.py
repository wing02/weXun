# -*- coding=utf-8 -*-
import sys, os, codecs, re
import pdb
import matplotlib.pyplot as plt
 
reload(sys) 
sys.setdefaultencoding('utf-8')
 
import cProfile
import urllib2
 
 
class TextExtract(object):
    re_title = re.compile(r'<title>(.*?)</title>', re.I|re.U|re.S)
    re_body = re.compile(r'<body[^>]*>.*</body>', re.I|re.U|re.S)
    re_doc_type = re.compile(r'<!DOCTYPE.*?>', re.I|re.U|re.S)
    re_comment = re.compile(r'<!--.*?-->', re.I|re.U|re.S)
    re_js = re.compile(r'<script[^>]*>.*?</script>', re.I|re.U|re.S)
    re_img = re.compile(r'<img[^>]*>',re.I|re.S|re.U)
    re_css = re.compile(r'<style[^>]*>.*?</style>', re.I|re.U|re.S)
    re_special = re.compile(r'&.{2,8};|&#.{2,8};', re.I|re.U|re.S)
    re_p = re.compile(r'<p>', re.I|re.U|re.S)
    re_up = re.compile(r'</p>', re.I|re.U|re.S)
    re_other = re.compile(r'<[^>]*>', re.I|re.U|re.S)
     
    blockHeight = 11
    imgLength=20

    def __init__(self, new_html, doRemoveLF=True):
        self.doRemoveLF=doRemoveLF
        self.html = new_html
        self.text_start = 0
        self.text_end = 0
        self.text_body = ''
        #self.blocks = []
        self.title = ''
        self.content = ''
        self.extract()
 
    def extract(self):
        self.extract_title()
        self.extract_body()
        self.remove_tags()
        self.extract_text()
        self.getUsedImgs()
     
    def extract_title(self):
        m = self.re_title.search(self.html)
        if m:
            self.title = m.group(1)
 
    def extract_body(self):
        m = self.re_body.search(self.html)
        if m:
            self.text_body = m.group()
 
    def remove_tags(self):
        self.text_body = self.re_doc_type.sub('', self.text_body)
        self.text_body = self.re_comment.sub('', self.text_body)
        self.text_body = self.re_js.sub('', self.text_body)
        self.text_body = self.re_css.sub('', self.text_body)
        self.text_body = self.re_special.sub('', self.text_body)
        self.replaceImg()
        if self.doRemoveLF:
            self.text_body = self.text_body.replace('\r\n','').replace('\n','')
        #self.text_body = self.re_p.sub('{p}', self.text_body)
        self.text_body = self.re_up.sub('{up}', self.text_body)
        self.text_body = self.re_other.sub('\n', self.text_body)

 
    def extract_text(self):
        lines = self.text_body.split('\n')
        line_len = len(lines)
        for i in xrange(0,line_len,1):
            lines[i] = re.sub(r'\s+', ' ', lines[i]).strip()
         
        for i in xrange(1,line_len-1,1):
            if len(lines[i]) > 0 and len(lines[i]) < 30 and 0 == len(lines[i-1]) and 0 == len(lines[i+1]):
                lines[i] = ''
 
        blocks=[]
        for i in xrange(0, len(lines)-self.blockHeight, 1):
            line_len = 0
            for j in xrange(0, self.blockHeight, 1):
                line_len += len(lines[i+j])
            blocks.append(line_len)
        
        if len(blocks)==0:
            self.content=''
            return
        #self.drawBlock(blocks)
        maxBlock=max(blocks)
        #minBlock=self.blockHeight
        minBlock=10
        peaks=[]

        rhs=0
        for i in range(len(blocks)):
            if blocks[i]>=maxBlock:
                if i<rhs:
                    continue
                lhs=i
                rhs=i
                while(blocks[lhs]>minBlock):
                    lhs-=1
                while(blocks[rhs]>minBlock and rhs<len(blocks)-1):
                    rhs+=1
                peaks.append((lhs+self.blockHeight,rhs))
        
        for peak in peaks:
            for i in range(peak[0],peak[1]):
                self.content+=lines[i]

    def drawBlock(self,blocks):
        x=range(len(blocks))
        plt.plot(x,blocks)
        plt.show()
        
    def replaceImg(self):
        self.imgSrcs=map(self.getImgSrc,self.re_img.findall(self.text_body))
        txts=self.re_img.split(self.text_body)
        self.text_body=txts[0]
        for i in range(len(txts)-1):
            self.text_body+='{img'+str(i)+'$'*self.imgLength+'}'
            self.text_body+=txts[i+1]

    def getImgSrc(self,img):
        src=re.search('src="(.*?)"',img)
        if src:
            return src.group(1)
        else:
            return ''

    def getUsedImgs(self):
        #pdb.set_trace()
        indexs=map(int,re.findall('{img(\d+)\$*}',self.content))
        self.content=re.sub('{img(\d+)\$*}','{img}',self.content)
        self.imgs=[]
        for index in indexs:
            self.imgs.append(self.imgSrcs[index])
        return self.imgs

        
 
if __name__ == "__main__":

    #url='http://ln.qq.com/a/20160723/003673.htm'
    #url='http://www.taiwan.cn/xwzx/la/201607/t20160723_11516742.htm'
    #url='http://www.gov.cn/xinwen/2016-07/23/content_5094173.htm'
    #url='http://zz.house.qq.com/a/20160724/004694.htm'
    #url='http://sznews.com/zhuanti/content/2016-08/04/content_13686753_11.htm'
    #url='http://yi.china.com/tuku/11177361/20160805/23208443.html'
    #url='http://www.bannedbook.org/bnews/topimagenews/20160808/568794.html'
    #url='http://news.qq.com/a/20160809/011891.htm'
    #url='http://stock.qq.com/a/20160809/043400.htm'
    #url='http://sc.people.com.cn/n2/2016/0818/c345535-28854712-10.html'
    #url='http://news.qq.com/a/20160827/000128.htm'
    #url='http://news.xinhuanet.com/politics/2016-07/24/c_1119270615.htm'
    #url='http://military.people.com.cn/n1/2016/0724/c1011-28580193.html'
    url='http://sc.people.com.cn/n2/2016/0817/c345537-28848447.html'
    proxied_request = urllib2.urlopen(url)

    #content = proxied_request.read().decode('gbk')
    content = proxied_request.read()
    content=content.decode('gbk')
    #f=open('qq','w')
    #f.write(content.encode('u8'))
    #f.close()

    #f=open('qq','r')
    #content=f.read().decode('u8')
    text_extract = TextExtract(content,True)
    print (text_extract.content)
    print (text_extract.imgs)
