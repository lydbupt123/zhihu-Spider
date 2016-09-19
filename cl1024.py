import urllib.request  
import re

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')
    return html

def getImg(html):
    reg = r'src="(.+?\.(jpg|png|jpeg))"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    x = 0
    for imgurl in imglist:
        print(imgurl[0])
        if imgurl[0][0]=='h':
            try:
                urllib.request.urlretrieve(imgurl[0],'%s.jpg' % x)
                x+=1
            except urllib.error.HTTPError as reason:
                print(reason)
                

html = getHtml("https://www.zhihu.com/question/22212644")
getImg(html)
