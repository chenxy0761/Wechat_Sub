# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from lxml import etree
from PIL import Image
import requests
import re
import time

from selenium import webdriver

# 注意URL的选择
url = 'https://www.newrank.cn/public/info/detail.html?account=shtt365'

cookie = {
    'Cookie': 'rmbuser=true; name=15601615046; useLoginAccount=true; token=AFEDF054FEF056BB6B73F502F00632E4; tt_token=true; UM_distinctid=16270aa4201155-03757b7e6ed69-4353468-100200-16270aa4203212; __root_domain_v=.newrank.cn; _qddaz=QD.aazmus.1v9gv0.jfc796eo; rmbuser=true; name=15601615046; useLoginAccount=true; token=AFEDF054FEF056BB6B73F502F00632E4; Hm_lvt_a19fd7224d30e3c8a6558dcb38c4beed=1522310874,1522310885,1522331039,1522373987; CNZZDATA1253878005=1453680831-1522306762-https%253A%252F%252Fwww.sogou.com%252F%7C1522371855; _qdda=3-1.1qd9sp; _qddab=3-jgtikk.jfda5z65; _qddamta_2852150610=3-0; _qddac=3-1.1qd9sp.jgtikk.jfda5z65; Hm_lpvt_a19fd7224d30e3c8a6558dcb38c4beed=1522374039; tt_token=true'
}
html = requests.get(url, cookies=cookie).content
soup = BeautifulSoup(html, "lxml")
names = str(soup.find("div", {"class": 'info-detail-head-weixin-name'}))
dd = names[names.index('<span>') + 6:names.index('<!--')]
test = str(soup.find("script",{"type":"text/javascript"}))
list = test[test.index('[')+2:test.index(']')-1]
lists = list.split("},{")
article_clicks_count=""
article_likes_count=0
rank_date=0
for data in lists:
    ll = data.split(',')
    for l in ll:
        if l.split(':')[0].strip("\"")=="article_clicks_count":
            article_clicks_count = l.split(':')[1].strip("\"")
        if l.split(':')[0].strip("\"")=="article_likes_count":
            article_likes_count = l.split(':')[1].strip("\"")
        if l.split(':')[0].strip("\"")=="rank_date":
            rank_date = l.split(':')[1].strip("\"").strip(" 00")
            # rank_date=time.strptime(str(rank_date),"%Y-%m-%d")
    print("微信id:"+"shtt365"+"   微信名:"+dd.strip()+"  总阅读数:"+article_clicks_count+"    点赞数:"+article_likes_count+" 日期:"+rank_date)





# test = soup.find("div","highcharts-tooltip")
# print(test)
# dd = str(names)[str(names).index('<span>') + 6:str(names).index('<!--')]
# print(dd.strip())
#
# browser = webdriver.Chrome()
# browser.get("")
# browser.find_element_by_id("trend_article_likes_count").click()
# names2 = soup.find("div", {"class": 'info-detail-rank-data-drawing-reading'})
# print(names2)
# browser.close()
