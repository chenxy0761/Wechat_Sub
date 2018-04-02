# -*- coding:utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.conf import settings

from Wechat_Sub.items import WecatItem


class WechatSub(scrapy.Spider):
    name = "newrank"
    allowed_domains = ["newrank.cn"]
    urls = []
    file = open("Wechat_Sub/util/wechatNames.txt")
    for title in file:
        # print(title)
        urls.append("https://www.newrank.cn/public/info/detail.html?account=" + title.strip())
    start_urls = urls
    # start_urls = ["https://www.newrank.cn/public/info/detail.html?account=helloshanghai2013"]
    cookie = settings['COOKIE']
    headers = {
        'Connection': 'keep - alive',  # 保持链接状态
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookie)

    def parse(self, response):
        try:
            sel = Selector(response)
            title = sel.xpath("//div[@class=\"info-detail-head-weixin-name\"]/span//text()").extract()
            id = sel.xpath("//div[@class=\"info-detail-head-weixin-num\"]/p/span//text()").extract()[0].split('：')[1]
            wechat_name = title[0].strip()
            script = str(sel.xpath("//script//text()").extract())
            list = script[script.index(':[') + 3:script.index(']') - 1]
            lists = list.split("},{")
            wechatItem = WecatItem()
            wechatItem['id'] = id
            wechatItem['name'] = wechat_name

            for data in lists:
                ll = data.split(',')
                for l in ll:
                    if l.split(':')[0].strip("\"") == "article_clicks_count":
                        wechatItem['click_count'] = l.split(':')[1].strip("\"")
                    if l.split(':')[0].strip("\"") == "article_likes_count":
                        wechatItem['likes_count'] = l.split(':')[1].strip("\"")
                    if l.split(':')[0].strip("\"") == "rank_date":
                        wechatItem['rank_date'] = l.split(':')[1].strip("\"")[0:-3]
                    # rank_date=time.strptime(str(rank_date),"%Y-%m-%d")
                if wechatItem['click_count'] == "" and wechatItem['likes_count'] == "" and wechatItem[
                    'rank_date'] == "":
                    return
                yield wechatItem
        except Exception as e:
            pass

        pass

    pass
