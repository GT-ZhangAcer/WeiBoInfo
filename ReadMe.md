# 抓取微博热点信息


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

exe--框架所需部分环境

data--数据存放目录

**_注意事项_**

1.需要自行安装geckodriver-v0.23.0-win64到虚拟环境或实体环境

2.若在等待JS之后出现错误 请尝试更改 JS、Driver的等待时间

3.data下的文件在WIndows下需要手动创建Utf-8编码格式 否则不能正确写入

**_API_**
