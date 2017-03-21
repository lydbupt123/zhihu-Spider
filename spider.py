import urllib.request  
import re
import os

path='E:\\pictures\\'

def mkdir(title):
    new_path=path+title

    isExists=os.path.exists(new_path)
    new_path=new_path.rstrip('.')
    new_path=new_path.rstrip(' ')
    print(new_path)
    if not isExists:
        os.makedirs(new_path)
    else:
        print("目录已经存在")
        return int(1)

    return new_path

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')
    reg = r'<tbody\sid="normalthread(?s).*?<th(?s).*?href="(thread.+?.html)(?s).*?>(.+?)</a>(?s).*?</tbody>'
    imgre = re.compile(reg)
    subhtml=re.findall(imgre,html)
    for page in subhtml:
        page=list(page)
        page[0]='http://www.cl864.com/'+str(page[0])
        #print(page)
        #print(type(page))
        getImg(page[0],page[1])
    reg=r'<span\sid="fd_page_bottom">(?s).*<a\shref="(.+?\.html)"\sclass="nxt"(?s).*?</span>'
    imgre = re.compile(reg)
    next_page=re.findall(imgre,html)
    print(next_page)
    return 'http://www.cl864.com/'+next_page[0]

def getImg(html,title):
    title=re.sub('[/\\\:\*\?"<>\|]','',title)
    new_path=mkdir(title)
    if new_path!=1:
        new_path+='\\'
        print(title)
        page = urllib.request.urlopen(html)
        html = page.read().decode('utf-8')
        reg = r'<img\sid="aimg_(?s).*?file="(.+?(\.|;)(jpg|png|jpeg))"(?s).*?>'
        imgre = re.compile(reg)
        imglist = re.findall(imgre,html)
        for i,imgurl in enumerate(imglist):
            try:
                print(imgurl[0])
                urllib.request.urlretrieve(imgurl[0],(new_path+'%s.jpg')%i)
            except TimeoutError:
                continue
            except urllib.error.HTTPError as reason:
                if reason.code==403:
                    opener=urllib.request.build_opener()
                    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(imgurl[0],(new_path+'%s.jpg')%i)
            except urllib.error.URLError as reason:
                print(reason)
            except:
                print('有问题！')

#test
#getImg('http://www.cl864.com/thread-934718-1-1.html','Test')
html="http://www.t66y.com/thread0806.php?fid=16"
for i in range(100):
    html = getHtml(html)

