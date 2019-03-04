# 抓取微博热点评论信息


_**信息收集**_

1.热点榜网页地址
  https://s.weibo.com/top/summary?


_**使用环境**_

Python 3.7

beautifulsuop4

lxml

Selenium

Firefox x64

_**目录结构**_

venv372x64win---虚拟环境目录

MainScript.py---主脚本

exe---框架所需部分环境

data---数据存放目录

scriptTool.py---工具集

DeBug--控制台输出记录存放目录

**_注意事项_**

1.需要自行安装geckodriver-v0.23.0-win64到虚拟环境或实体环境

2.若在等待JS之后出现错误 请尝试更改 JS、Driver的等待时间

3.data下的文件在Windows下需要手动创建Utf-8编码格式 否则不能正确写入

**_API_**

1、`MainScript.hotPointList 解析热点榜 返回指定热点链接、话题、以及热度` 

**传入对象**：int值-所选热点的序号 

例：1

**返回对象**：列表[热点链接、话题、热度]

例：['https://s.weibo.com/weibo?q=%23%E5%A7%9C%E4%B8%B9%E5%B0%BC%E5%B0%94%E8%A6%81%E6%B1%82%E8%A7%A3%E7%BA%A6%23&;Refer=top',

'姜丹尼尔要求解约',

'930085']

2、`MainScript.hotTexturl 解析话题搜索页内热门微博Url`

**传入对象**：str类型-搜索页Url
 
例：'https://s.weibo.com/weibo?q=%23%E5%A7%9C%E4%B8%B9%E5%B0%BC%E5%B0%94%E8%A6%81%E6%B1%82%E8%A7%A3%E7%BA%A6%23&amp;Refer=top'

**返回对象**：列表[微博详细页面Url 1、2、3...]

3、`MainScript.weiBoInfo 解析微博评论数据`

**传入对象**：str类型-微博详细页Url,Selenium的浏览器对象

**返回对象**：在./data目录下生成data.txt 并追加写入获取的评论数据


