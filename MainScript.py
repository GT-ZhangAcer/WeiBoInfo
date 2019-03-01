# encoding:utf-8
from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from scriptTool import workPath
import re

urlMain = "https://s.weibo.com"


# 解析热点榜
def hotPointList(i):
    i += 1
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
    # print(info)

    return info
    # info中第一个为链接 第二个为话题标题 第三为热度


# 解析首个热门微博
def hotTexturl(url):
    html = urlopen(urlMain + url)
    html_BSObj = BeautifulSoup(html, "lxml")  # 链接对象
    # 查找父节点 得到热门微博
    find_src = html_BSObj.find(attrs={"class": "icon-title icon-star"}).parent.parent.parent.parent
    # 找到时间对应的Url
    urlinfo = str(find_src.find_all(attrs={"target": "_blank"})).split('href="')[-1]
    urlinfo = "https:" + urlinfo.split('"')[0]
    # 测试输出
    # print(urlinfo)
    return urlinfo


'''
def hotTexturl_NoKey(url):
    html = request.Request(url)
    # 免登陆请求网页 使用安卓UA避免报错
    html.add_header("User-Agent",
                    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.")
    html = urlopen(html)
    html_BSObj = BeautifulSoup(html, "lxml")  # 链接对象
    url = str(html_BSObj).split('"text": "<a  href=\\"https://m.weibo.cn/search?')[1]
    url = "https://m.weibo.cn/search?" + url.split("\\")[0]

    # 测试输出
    print(url)
    return url
'''


def weiBoInfo(url, driver):
    driver.get(url)
    print("正在等待JS...")
    driver.implicitly_wait(10)  # 等待JS加载时间
    print("正在等待Driver...")
    time.sleep(15)
    page = driver.page_source  # 保存网页源码
    html_BSObj = BeautifulSoup(page, "lxml")  # 链接对象
    find_text = html_BSObj.find(attrs={"class": "WB_text W_f14"})
    find_text = re.findall('(?<=/.>).*?(?=<)', str(find_text))  # (?<=#</a>)前项匹配#</a> .*?匹配中间任意字符防止出界 (?=<)后项匹配

    find_commentinfo = html_BSObj.findAll(attrs={"class": "list_li S_line1 clearfix"})
    find_Obj = BeautifulSoup(str(find_commentinfo), "lxml")
    find_ID = find_Obj.findAll(attrs={"class": "WB_text"})  # 提取 ID和评论并清洗
    find_Time = find_Obj.find_all(attrs={"class": "WB_from S_txt2"})  # 提取时间并清洗
    find_comment = re.findall('(?<=</a>：).*?(?=<)', str(find_ID))  # 清洗评论
    find_ID = re.findall('(?<=usercard=).*?(?=</a>)',str(find_ID))#清洗ID

    find_Time=re.findall('(?<=S_txt2">).*?(?=</div>)',str(find_Time))

    timea = time.strftime("%Y-%m-%d-%H:%M", time.localtime())#获取当前时间
    # 测试输出
    #print("微博内容为：" + str(find_text))

    # print(find_comment)
    #print(find_ID)
    #print(find_comment)


    #print(find_Time)
    # 写入文件

    with open("./data/ocrData.txt", 'at', encoding='utf-8') as f:  # wt为不能追加 此处用at
        f.writelines("时间为：" + str(timea) + "\n")
        f.writelines("微博内容为：" + str(find_text) + "\n")
        if (len(find_ID) == len(find_comment) and len(find_Time)):
            print("数据写入--OK!")
        else:
            print("网络出现延时 数据可能不完整！")
        num=0
        if(len(find_ID)>len(find_comment)):
            num=len(find_comment)
        elif(len(find_ID)<len(find_comment)):
            num=len(find_ID)
        else:
            num=len(find_Time)
        for i in range(num):
            f.write(str(find_ID[i])+"\t")
            f.write(str(find_comment[i])+"\t")
            f.writelines(str(find_Time[i])+"\n")
        print("数据写入--OK!")

# 启动火狐浏览器
firefoxOpt = Options()  # 载入配置
firefoxOpt.add_argument("--headless")
print("启动浏览器ing...")
driver = webdriver.Firefox(workPath() + 'exe/core/', firefox_options=firefoxOpt)
for i in range(1,40):

    try:
        info = hotPointList(i)  # 加载热点排行榜url传递给热门微博文章提取函数
        print("|第"+str(i)+"个题标题为：" + info[1] + "|热度为：" + info[2])
        hoturl = hotTexturl(info[0])  # 热点话题链接

    # 话题链接传入
        weiBoInfo(hoturl, driver)
    except:
        continue
