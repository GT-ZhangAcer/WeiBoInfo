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
    info = urlMain + top_varurl, top_title, top_hotNum

    # 测试输出
    print(info)

    return info
    # info中第一个为链接 第二个为话题标题 第三为热度


# 解析话题搜索页内热门微博
def hotTexturl(url):
    html = urlopen(url)
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
    find_text = html_BSObj.find(attrs={"class": "WB_text W_f14"})  # 查找标题
    find_text = find_text.contents[0]  # 录入标题

    find_commentinfo = html_BSObj.findAll(attrs={"class": "list_li S_line1 clearfix"})  # 定位评论区

    # 定义数据列表
    find_IDList = []
    find_commentList = []
    find_TimeList = []
    # 测试输出
    '''
    # print(len(find_commentinfo[0]))
    for i in range(len(find_commentinfo)):
        print(str(i) + "---" + str(find_commentinfo[i].contents))
    '''
    for i in range(len(find_commentinfo)):
        try:
            find_commentChild = find_commentinfo[i].contents[9]  # 定位主评论区
            find_Obj = BeautifulSoup(str(find_commentChild), "lxml")
            find_ID = find_Obj.find(attrs={"class": "WB_text"})  # 提取 ID和评论并清洗
            find_Time = find_Obj.find(attrs={"class": "WB_from S_txt2"})  # 提取时间并清洗
            find_commentList.append(re.findall('(?<=</a>：).*?(?=<)', str(find_ID)))  # 清洗评论
            find_IDList.append(re.findall('(?<=usercard=).*?(?=</a>)', str(find_ID)))  # 清洗ID

            find_TimeList.append(re.findall('(?<=S_txt2">).*?(?=</div>)', str(find_Time)))
            # print(str(i) + "---")
        except:
            continue

    # 测试输出
    # print("微博内容为：" + str(find_text))
    # print(find_commentinfo)
    # print(find_IDList)
    # print(find_commentList)
    # print(find_TimeList)
    # print(len(find_IDList), len(find_commentList), len(find_TimeList))
    # 写入文件

    with open("./data/Data.txt", 'at', encoding='utf-8') as f:  # wt为不能追加 此处用at
        f.writelines(str(find_text) + "\n" + "--------------------" + "\n")
        if (len(find_IDList) == len(find_commentList) and len(find_TimeList)):
            print("数据写入--OK!")
        else:
            print("网络出现延时 数据可能不完整！")
        num = 0
        if (len(find_IDList) > len(find_commentList)):
            num = len(find_commentList)
        elif (len(find_IDList) < len(find_commentList)):
            num = len(find_IDList)
        else:
            num = len(find_TimeList)
        for i in range(num):
            f.write(str(find_IDList[i]) + "\t")
            f.write(str(find_commentList[i]) + "\t")
            f.writelines(str(find_TimeList[i]) + "\n")
            print("数据写入--OK!")


# 启动火狐浏览器
def __init__():
    firefoxOpt = Options()  # 载入配置
    # firefoxOpt.add_argument("--headless")
    print("启动浏览器ing...")
    driver = webdriver.Firefox(workPath() + 'exe/core/', firefox_options=firefoxOpt)

    # 生产模式
    for i in range(1, 20):

        try:
            info = hotPointList(i)  # 加载热点排行榜url传递给热门微博文章提取函数
            writeinfo = ("--------------------" + "\n" + "|第" + str(i) + "个题标题为：" + info[1] + "|热度为：" + info[2])
            timea = time.strftime("%Y-%m-%d-%H:%M", time.localtime())  # 获取当前时间
            with open("./data/Data.txt", 'at', encoding='utf-8') as f:  # wt为不能追加 此处用at
                f.writelines("\n" + "时间为：" + str(timea) + "\n")
                f.writelines("微博内容为：" + writeinfo + "\n")
            hoturl = hotTexturl(info[0])  # 热点话题链接

            # 话题链接传入
            weiBoInfo(hoturl, driver)
        except:
            print("第%s出现错误 错误代码Error---000" % i)
            continue

    # 调试模式
    '''
    info = hotPointList(1)  # 加载热点排行榜url传递给热门微博文章提取函数
    writeinfo = ("--------------------" + "\n" + "|第" + str(1) + "个题标题为：" + info[1] + "|热度为：" + info[2])

    timea = time.strftime("%Y-%m-%d-%H:%M", time.localtime())  # 获取当前时间
    with open("./data/ocrData.txt", 'at', encoding='utf-8') as f:  # wt为不能追加 此处用at
        f.writelines("时间为：" + str(timea) + "\n")
        f.writelines("微博内容为：" + writeinfo + "\n")
    hoturl = hotTexturl(info[0])  # 热点话题链接

    # 话题链接传入
    weiBoInfo(hoturl, driver)
    '''


__init__()
