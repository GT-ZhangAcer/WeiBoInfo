# encoding:utf-8
from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import scriptTool
import re

urlMain = "https://s.weibo.com"
filePath = "./data/Data.txt"


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
    print("OUT_INFO_Url:", info[0], "\nOUT_INFO_Title:", info[1], "\nOUT_INFO_热度:", info[2])

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
    print("ACT_INFO:等待JS...")
    driver.implicitly_wait(10)  # 等待JS加载时间
    print("ACT_INFO:等待Driver...")
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

    # for i in range(len(find_commentinfo)):
    #    print(str(i) + "---" + str(find_commentinfo[i].contents))

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
    # scriptTool.debug_SEcontents_C(find_text)
    # print("微博内容为：" + str(find_text))
    # print(find_commentinfo)
    # print(find_IDList)
    # print(find_commentList)
    # print(find_TimeList)
    print("OUT_INFO_Len:", len(find_IDList), len(find_commentList), len(find_TimeList))
    # 写入文件

    with open(filePath, 'at', encoding='utf-8') as f:  # wt为不能追加 此处用at
        f.writelines(str(find_text).strip() + "\n" + "--------------------" + "\n")
        if (len(find_IDList) == len(find_commentList) and len(find_TimeList)):
            print("OUT_INFO_数据写入:--OK!")
        else:
            print("===ERROR_003===：网络出现延时，数据可能不完整！")
            f.writelines("===ERROR_003===：网络出现延时，数据可能不完整！\n")
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

            if (i == num):
                print("OUT_INFO_数据写入:--OK!")


# 启动火狐浏览器
def __init__():
    # 生产模式
    def work():
        # 启动浏览器
        try:
            firefoxOpt = Options()  # 载入配置
            firefoxOpt.add_argument("--headless")
            print("ACT_INFO:启动浏览器ing...")
            driver = webdriver.Firefox(scriptTool.workPath() + 'exe/core/', firefox_options=firefoxOpt)
            print("OUT_INFO:浏览器启动成功！")
        except:
            print("===ERROR_002===:浏览器配置出现错误 程序即将退出！")
            return "002"
        timeb = str(time.strftime("%Y-%m-%d-%H-%M", time.localtime()))

        # 创建文件
        try:
            with open("./data/%sData.txt" % timeb, 'at', encoding='utf-8') as f:
                f.writelines("本次抓取的时间为：%s\n" % timeb)
            global filePath
            filePath = "./data/%sData.txt" % timeb
        except:
            print("===ERROR_004===：写入文件出现错误")
            return "004"

        Num = input("OUT_INFO:输入需要抓取话题的数量\nIN_INT_Number:")
        for i in range(1, int(Num)+1):
            print("OUT_INFO_序列:正在抓取第%s个话题,当前进度为：" % i + str(
                str(float(i) / float(Num) * 100)[:3]) + "%")  # 此处表达式为输出百分比
            # 抓取信息
            try:
                info = hotPointList(i)  # 加载热点排行榜url传递给热门微博文章提取函数
                writeinfo = ("--------------------" + "\n" + "|第" + str(i) + "个题标题为：" + info[1] + "|热度为：" + info[2])
                timea = time.strftime("%Y-%m-%d-%H:%M", time.localtime())  # 获取当前时间

                with open(filePath, 'at', encoding='utf-8') as f:  # wt为不能追加 此处用at
                    f.writelines("URL:" + str(info[0]) + "\n")
                    f.writelines("OUT_INFO_时间：" + str(timea) + "\n")
                    f.writelines("微博内容为：" + writeinfo + "\n")
                hoturl = hotTexturl(info[0])  # 热点话题链接

                # 话题链接传入
                weiBoInfo(hoturl, driver)
            except:
                print("===ERROR_000===:第%s个话题抓取出现错误\n请检查网络至新浪服务器的连接或进行等待" % i)
                continue
        print("OUT_INFO:执行完毕！")

    # 调试模式
    def debug():
        print("ACT_INFO:启动浏览器ing...")
        driver = webdriver.Firefox(scriptTool.workPath() + 'exe/core/')
        info = hotPointList(1)  # 加载热点排行榜url传递给热门微博文章提取函数
        writeinfo = ("--------------------" + "\n" + "|第" + str(1) + "个题标题为：" + info[1] + "|热度为：" + info[2])

        timea = time.strftime("%Y-%m-%d-%H:%M", time.localtime())  # 获取当前时间
        with open("./data/Data.txt", 'at', encoding='utf-8') as f:  # wt为不能追加 此处用at
            f.writelines("OUT_INFO_时间：" + str(timea) + "\n")
            f.writelines("OUT_INFO_微博内容：" + writeinfo + "\n")
        hoturl = hotTexturl(info[0])  # 热点话题链接

        # 话题链接传入
        weiBoInfo(hoturl, driver)

    # 模式选择
    work()


__init__()
