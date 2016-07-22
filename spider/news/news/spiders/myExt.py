# -*- coding=utf-8 -*-
import sys, os, codecs, re
import pdb
import matplotlib.pyplot as plt
 
#reload(sys) 
#sys.setdefaultencoding('utf-8')
 
import cProfile
import urllib2
 
 
class TextExtract(object):
    re_title = re.compile(r'<title>(.*?)</title>', re.I|re.U|re.S)
    re_body = re.compile(r'<body[^>]*>.*</body>', re.I|re.U|re.S)
    re_doc_type = re.compile(r'<!DOCTYPE.*?>', re.I|re.U|re.S)
    re_comment = re.compile(r'<!--.*?-->', re.I|re.U|re.S)
    re_js = re.compile(r'<script.[^>]*>.*?</script>', re.I|re.U|re.S)
    re_img = re.compile(r'<img.[^>]*>')
    re_css = re.compile(r'<style[^>]*>.*?</style>', re.I|re.U|re.S)
    re_special = re.compile(r'&.{2,8};|&#.{2,8};', re.I|re.U|re.S)
    re_other = re.compile(r'<[^>]*>', re.I|re.U|re.S)
     
    BLOCK_HEIGHT = 3
    def __init__(self, new_html, join=True):
        self.html = new_html
        self.join = join
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
        self.text_body = self.re_other.sub('', self.text_body)

 
    def extract_text(self):
        lines = self.text_body.split('\n')
        line_len = len(lines)
        for i in xrange(0,line_len,1):
            lines[i] = re.sub(r'\s+', ' ', lines[i]).strip()
         
        for i in xrange(1,line_len-1,1):
            if len(lines[i]) > 0 and len(lines[i]) < 30 and 0 == len(lines[i-1]) and 0 == len(lines[i+1]):
                lines[i] = ''
 
        blocks=[]
        for i in xrange(0, len(lines)-self.BLOCK_HEIGHT, 1):
            line_len = 0
            for j in xrange(0, self.BLOCK_HEIGHT, 1):
                line_len += len(lines[i+j])
            blocks.append(line_len)
        
        maxBlock=max(blocks)*2/3
        minBlock=self.BLOCK_HEIGHT*1
        peaks=[]

        rhs=0
        for i in range(len(blocks)):
            if blocks[i]>maxBlock:
                if i<rhs:
                    continue
                lhs=i
                rhs=i
                while(blocks[lhs]>minBlock):
                    lhs-=1
                while(blocks[rhs]>minBlock):
                    rhs+=1
                peaks.append((lhs+self.BLOCK_HEIGHT,rhs))
        
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
            self.text_body+='IMG'+str(i)+'$'
            self.text_body+=txts[i+1]

    def getImgSrc(self,img):
        src=re.search('src="(.*?)"',img)
        if src:
            return src.group(1)
        else:
            return ''

    def getUsedImgs(self):
        #pdb.set_trace()
        indexs=map(int,re.findall('IMG(\d+)\$',self.content))
        self.imgs=[]
        for index in indexs:
            self.imgs.append(self.imgSrcs[index])
        return self.imgs


        
 
if __name__ == "__main__":
    #url = 'http://news.xinhuanet.com/politics/2016-07/21/c_129167395.htm'
    #url='http://news.xinhuanet.com/fortune/2016-07/21/c_129167394.htm'
    #url='http://military.people.com.cn/n1/2016/0722/c1011-28577225.html'
    #url='http://military.people.com.cn/n1/2016/0722/c1011-28575929.html'
    url='http://news.qq.com/a/20160722/033954.htm'
    #url = 'http://news.qq.com/a/20160722/001785.htm'
    proxied_request = urllib2.urlopen(url)
    status_code = proxied_request.code
    mimetype = proxied_request.headers.typeheader or mimetypes.guess_type(url)
    content = proxied_request.read().decode('gbk')
    #encoding = proxied_request.headers['content-type'].split('charset=')[-1]
    #ucontent = unicode(content, encoding)
    text_extract = TextExtract(content)
    print (text_extract.content)
    print (text_extract.imgs)
