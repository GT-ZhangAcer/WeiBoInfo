# encoding:utf-8
import re

strr='<div class="WB_text W_f14" nick-name="济南市济南事" node-type="feed_list_content"><a class="a_topic" extra-data="type=topic" href="http://s.weibo.com/weibo?q=%23%E6%95%99%E5%B8%88%E8%B5%84%E6%A0%BC%E8%AF%81%E9%9D%A2%E8%AF%95%E6%88%90%E7%BB%A9%23" render="ext" suda-uatrack="key=topic_click&amp;value=click_topic" target="_blank">#教师资格证面试成绩#</a>教师资格证面试成绩开始查询了，7S内转走点赞这逢考必过真言符咒，轻松必过线，助你圆梦！<img alt="[中国赞]" class="W_img_face" render="ext" src="//img.t.sinajs.cn/t4/appstyle/expression/ext/normal/6d/2018new_zhongguozan_org.png" title="[中国赞]" type="face"/><img alt="[中国赞]" class="W_img_face" render="ext" src="//img.t.sinajs.cn/t4/appstyle/expression/ext/normal/6d/2018new_zhongguozan_org.png" title="[中国赞]" type="face"/>'
#find_text=re.findall('#</a>.*<',str(strr))
find_text=re.findall('(?<=#</a>).*?(?=<)',strr)#(?<=#</a>)前项匹配#</a> .*?匹配中间任意字符 (?=<)后项匹配
print(find_text)