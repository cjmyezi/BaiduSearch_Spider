# -*- coding: utf-8 -*-
import scrapy
from BaiduSearch_Spider.items import BaidunewsSpiderItem

from time import sleep
from BaiduSearch_Spider.body_path import *


class BaiduspiderSpider(scrapy.Spider):
    name = 'newsspider'
    # allowed_domains = ['http://news.baidu.com/']

    def start_requests(self):
        keyword="中山大学"
        begin_page = 0
        end_page = 25
        start_urls1 = "http://news.baidu.com/ns?word=中山大学&pn={0}&cl=2&ct=0&tn=newsdy&rn=10&ie=utf-8&bt=1514736000&et=1558195199"
        start_urls2 = "https://news.baidu.com/ns?word=%E5%8F%8C%E9%B8%AD%E5%B1%B1%20%2B%E4%B8%AD%E5%B1%B1%E5%A4%A7%E5%AD%A6&pn={0}&cl=2&ct=0&tn=news&rn=10&ie=utf-8&bt=0&et=0"
        for page in range(begin_page,end_page):# 一页链接数量由参数&rn=决定
            U = start_urls1.format(page*10)  
            # sleep(0.5)  #设置一个翻页的时间，太快了不好
            yield scrapy.Request(url = U,meta = {'keyword':keyword},callback = self.parse,dont_filter=True)
    
    def parse(self,response):
        for section in response.xpath('//div[@class="result" and @id]'):
            item = BaidunewsSpiderItem()
            item['keyword']=response.meta['keyword'] # 标注关键词
            try:
                info = section.xpath('.//a')[0]
                item['link'] = info.xpath('@href').extract()[0]
            except:
                item['link']=""

            try:
                res_title=section.xpath('.//h3/a')
                item['title']=(res_title[0].xpath('string(.)').extract_first()).strip('\n\t \'')
            except:
                item['title']=""
 
            try:
                b=section.xpath('.//div[@class="c-summary c-row " ]')
                if len(b)==0:
                    b=section.xpath('.//div[@class="c-summary c-row c-gap-top-small"]')
                S=b.xpath('string(.)').extract()[0]
                S=S.replace("\n"," ").replace("\t"," ").replace("\xa0"," ")
                List = S.split()
                List.pop() #去除百度快照
                item['platform'] = List[0]
                item['date'] = List[1]
                item['time'] = List[2]
                item['brief'] = "".join(List[3:])
                
            except:
                item['date']=""
                item['platform']=""
                item['brief']=""
                item['time']=""
            yield scrapy.Request(url = item['link'],meta = {'item':item},callback = self.parse_next,dont_filter=True)

    def parse_next(self,response): # 爬取正文的深度只有一层，所以如果正文中有翻页就只能爬取第一页的内容
        item = response.meta['item']
        item['link']=response.url #获取真实的url地址 地址为空则直接返回空的item
        if item['link']=='':
            yield item

        b=[]# 爬取正文的字符串列表
        string="" # 目标正文的字符串
        for path_str in path_list:
            a = response.xpath(path_str)
            if len(a)!=0: # 爬取正文数据 找到了就分析，否则继续寻找
                b=a.xpath('string(.)').extract()
                string="".join(b)
                if item['keyword'] in string: # 爬取到了有用的正文就可以离开循环
                    break
                else:
                    string="" #否则清空正文字符串 继续循环查找
        item['body']=string.replace('\n',"").replace('\t',"").replace(" ","").replace("\r","") # 去除没用的关键字
        yield item 