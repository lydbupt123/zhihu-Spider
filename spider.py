import urllib.request  
import re
import os
import requests

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

    return new_path

def getHtml(url):
    proxy = {"http":"http://127.0.0.1:1080","https":"https://127.0.0.1:1080"}
    response = requests.get(url,proxies = proxy,verify=False)
    response.encoding='gbk'
    html=response.text
    reg = r'<a\shref="(htm_data.+?\.html)"'
    imgre = re.compile(reg)
    subhtml=re.findall(imgre,html)
    for page in subhtml:
        #print(page)
        page='http://www.t66y.com/'+str(page)
        getImg(page)
        '''
    reg=r'<span\sid="fd_page_bottom">(?s).*<a\shref="(.+?\.html)"\sclass="nxt"(?s).*?</span>'
    imgre = re.compile(reg)
    next_page=re.findall(imgre,html)
    print(next_page)
    return 'http://www.cl864.com/'+next_page[0]'''

def getImg(url):
    proxy = {"http":"http://127.0.0.1:1080","https":"https://127.0.0.1:1080"}
    response = requests.get(url,proxies = proxy,verify=False)
    response.encoding='gbk'
    html=response.text
    title_reg=r'<h4>(.*?)</h4>'
    title_r=re.compile(title_reg)
    title=re.findall(title_r,html)
    if len(title)!=1:
        print("此页面找不到Title：")
        print(url)
    else:
        title=re.sub('[/\\\:\*\?"<>\|]','',title[0])
        new_path=mkdir(title)
        print(new_path)
        new_path+='\\'
        reg = r"<input\ssrc='(.+?\.jpg)'"
        imgre = re.compile(reg)
        imglist = re.findall(imgre,html)
        for i,imgurl in enumerate(imglist):
            print(imgurl)
            try:
                img=requests.get(imgurl,proxies = proxy,verify=False)
                img_download=open((new_path+'%s.jpg')%i,'wb').write(img.content)
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
#getImg('http://www.t66y.com/htm_data/16/1703/2312881.html')
html="http://www.t66y.com/thread0806.php?fid=16"
#for i in range(100):
html = getHtml(html)

