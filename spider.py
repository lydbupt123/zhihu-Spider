import urllib.request  
import re
import os
import requests
import threading
from time import ctime

path='G:\\pictures\\'

def mkdir(title):
    new_path=path+title

    isExists=os.path.exists(new_path)
    new_path=new_path.rstrip('.')
    new_path=new_path.rstrip(' ')
    if not isExists:
        os.makedirs(new_path)
    else:
        print("目录已经存在")
        return 'Exist'

    return new_path

def getHtml(url):
    proxy = {"http":"http://127.0.0.1:1080","https":"https://127.0.0.1:1080"}
    response = requests.get(url,proxies = proxy)
    response.encoding='gbk'
    html=response.text
    next_reg=r'<a>(?:.*?)<input(?:.*?)<a\shref="(.+)">下一頁'
    next_url=re.compile(next_reg)
    next_url=re.findall(next_url,html)
    reg = r'<a\shref="(htm_data.+?\.html)"'
    imgre = re.compile(reg)
    subhtml=re.findall(imgre,html)
    for i in range(len(subhtml)):
        subhtml[i]='http://www.t66y.com/'+str(subhtml[i])
    return subhtml,list(set(next_url))

def getImg(url):
    #url=url['url']
    proxy = {"http":"http://127.0.0.1:1080","https":"https://127.0.0.1:1080"}
    response = requests.get(url,proxies = proxy)
    response.encoding='gbk'
    html=response.text
    #print(html)
    title_reg=r'<title>(.*?)</title>'
    title_r=re.compile(title_reg)
    title=re.findall(title_r,html)
    if len(title)!=1:
        print("此页面找不到Title：")
        print(url)
    else:
        title=re.sub('[/\\\:\*\?"<>\|]','',title[0])
        new_path=mkdir(title)
        if new_path!='Exist':
            new_path+='\\'
            reg = r"<input\ssrc='(.+?\.(jpg|gif|jpeg|png))'"
            imgre = re.compile(reg)
            imglist = re.findall(imgre,html)
            for i,imgurl in enumerate(imglist):
                try:
                    img=requests.get(imgurl[0],proxies = proxy)
                    img_download=open((new_path+'%s.jpg')%i,'wb').write(img.content)
                except TimeoutError:
                    continue
                except urllib.error.HTTPError as reason:
                    print(reason)
                    '''if reason.code==403:
                        opener=urllib.request.build_opener()
                        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                        urllib.request.install_opener(opener)
                        urllib.request.urlretrieve(imgurl[0],(new_path+'%s.jpg')%i)'''
                except urllib.error.URLError as reason:
                    print(reason)
                except:
                    print(imgurl[0])
                    print('有问题！')

def main():
    html="http://www.t66y.com/thread0806.php?fid=16&search=&page=12"
    
    for num in range(10):
        threads=[]
        subhtml,next_page=getHtml(html)
        for sh in subhtml:
            sh={'url':sh}
            t=threading.Thread(target=getImg,kwargs=sh)
            threads.append(t)
        for i,t in enumerate(threads):
            t.start()
        print('All Start At:'+ctime())

        for i,t in enumerate(threads):
            t.join()
            print('Thread %s Finished!'%i)

        if len(next_page)==1:
            html="http://www.t66y.com/"+next_page[0]
        else:
            print("沒有找到下一頁")
            break

    print('All Done At:'+ctime())

if __name__=='__main__':
    main()

