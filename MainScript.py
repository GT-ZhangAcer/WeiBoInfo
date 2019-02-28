from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import re

urlMain="https://s.weibo.com"

#解析热点榜
def hotPointList(i):
    i+=1
    html = urlopen("https://s.weibo.com/top/summary?")
    html_BSObj = BeautifulSoup(html, "lxml")  # 链接对象
    find_src = html_BSObj.find_all(attrs={"class": "td-02"})
    top_src = str(find_src).split(",")[i]  # 提取第二个热点信息列表（第一往往为置顶）
    top_info = top_src.split("<")[2:]  # 提取主要信息
    # 提取链接
    top_varurl = top_info[0].split("\"")[1]
    # 提取标题
    top_title = top_info[0].split(">")[1]
    # 提取热度数据
    top_hotNum = top_info[2].split(">")[1]
    info = top_varurl, top_title, top_hotNum

    # 测试输出
    #print(info)

    return info
    # info中第一个为链接 第二个为标题 第三为热度

#解析首个热门微博
def hotTexturl(url):
    html = urlopen(urlMain+url)
    html_BSObj = BeautifulSoup(html, "lxml")  # 链接对象
    #查找父节点 得到热门微博
    find_src = html_BSObj.find(attrs={"class": "icon-title icon-star"}).parent.parent.parent.parent
    #找到时间对应的Url
    urlinfo=str(find_src.find_all(attrs={"target": "_blank"})).split('href="')[-1]
    urlinfo="https:"+urlinfo.split('"')[0]
    # 测试输出
    print(urlinfo)
    return urlinfo

def text(url):
    html = urlopen(url+"&type=comment#_rnd1551365282864")
    html_BSObj = BeautifulSoup(html, "lxml")  # 链接对象
    find_text = html_BSObj.find_all(attrs={"class": "WB_text W_f14"})
    print(html_BSObj)
    print(find_text)


#i = input("想提取第几条热点的信息呢")
info = hotPointList(1)#加载热点排行榜url传递给热门微博文章提取函数
hoturl=hotTexturl(info[0])
text(hoturl)#解析热门微博链接 传递给文章分析函数

'''html=urlopen(url)
htmlObj=BeautifulSoup(html,"lxml")
find_img=htmlObj.findAll("img",{"src":re.compile("[a-z]*")})
x=0
for pri in find_img:
    x=x+1
    print(pri.attrs["src"])'''
