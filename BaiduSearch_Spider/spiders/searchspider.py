# -*- coding: utf-8 -*-
import scrapy
from BaiduSearch_Spider.items import BaidusearchSpiderItem

from time import sleep
from BaiduSearch_Spider.body_path import *


class BaiduspiderSpider(scrapy.Spider):
    name = 'searchspider'
    count=0
    # allowed_domains = ['http://news.baidu.com/']

    def start_requests(self):
        keyword="双鸭山"
        begin_page = 0
        end_page = 76
        start_urls1 = "https://www.baidu.com/s?wd=%22%E5%8F%8C%E9%B8%AD%E5%B1%B1%22%20(%E4%B8%AD%E5%B1%B1%E5%A4%A7%E5%AD%A6)&pn={}&oq=%22%E5%8F%8C%E9%B8%AD%E5%B1%B1%22%20(%E4%B8%AD%E5%B1%B1%E5%A4%A7%E5%AD%A6)&tn=baiduadv&ie=utf-8&usm=1&rsv_pq=a2d05e1b00011aa3&rsv_t=0a5dGSMwxGbAMdlgZGZW%2F3p3LDtI0ZeS6zmvqogwaTML8EFfB1DqdRSHtCC8f50"
        for page in range(begin_page,end_page):# 一页链接数量由参数&rn=决定
            U = start_urls1.format(page*10)  
            # sleep(0.5)  #设置一个翻页的时间，太快了不好
            yield scrapy.Request(url = U,meta = {'keyword':keyword},callback = self.parse,dont_filter=True)
    
    def parse(self,response):
        list1 = response.xpath('//div[@class="result-op c-container xpath-log"]')
        list2 = response.xpath('//div[@class="result c-container "]')
        # print("\n\n\n")
        # print(list2)
        # print("\n\n\n")
        for section in list2:
            item = BaidusearchSpiderItem()
            item['keyword']=response.meta['keyword'] # 标注关键词
            item['number']=self.count
            self.count+=1
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
                b=section.xpath('.//div[@class="c-abstract" ]')
                if len(b)==0:
                    b=section.xpath('.//div[@class="c-summary c-row c-gap-top-small"]')
                S=b.xpath('string(.)').extract()[0]
                S=S.replace("\n"," ").replace("\t"," ").replace("\xa0"," ") # 用空格隔开方便下一步进行split
                List = S.split()
                List.pop() #去除百度快照
                if (List[0][0]).isdigit(): # 判断第一个是不是时间
                    item['time'] = List[0]
                    item['brief'] = ("".join(List[1:])).lstrip("= ")
                else:
                    item['time'] = ""
                    item['brief'] = ("".join(List[:])).lstrip("= ")
            except:
                item['time']=""
                item['brief']=""
            yield item
            # yield scrapy.Request(url = item['link'],meta = {'item':item},callback = self.parse_next,dont_filter=True)

        for section in list1:
            item = BaidusearchSpiderItem()
            item['number']=self.count
            self.count+=1
            item['keyword']=response.meta['keyword'] # 标注关键词
            try:
                info = section.xpath('.//h3/a')[0]
                item['link'] = info.xpath('@href').extract()[0]
            except:
                item['link']=""

            try:
                res_title=section.xpath('.//h3/a')
                item['title']=(res_title[0].xpath('string(.)').extract_first()).strip('\n\t \'')
            except:
                item['title']=""
            try:
                b=section.xpath('.//div[@class="c-row"]')
                S=b.xpath('string(.)').extract()[0]
                S=S.replace("\n"," ").replace("\t"," ").replace("\xa0"," ") # 用空格隔开方便下一步进行split
                List = S.split()
                List.pop() #去除更多
                item['time']="" # 这种讯息一般没有时间
                item['brief'] = ("".join(List[:])).lstrip("= ")
            except:
                item['time']=""
                item['brief']=""
            yield item
            # yield scrapy.Request(url = item['link'],meta = {'item':item},callback = self.parse_next,dont_filter=True)

    # def parse_next(self,response): # 爬取正文的深度只有一层，所以如果正文中有翻页就只能爬取第一页的内容
    #     item = response.meta['item']
    #     item['link']=response.url #获取真实的url地址 地址为空则直接返回空的item
    #     if item['link']=='':
    #         yield item

    #     b=[]# 爬取正文的字符串列表
    #     string="" # 目标正文的字符串
    #     for path_str in path_list:
    #         a = response.xpath(path_str)
    #         if len(a)!=0: # 爬取正文数据 找到了就分析，否则继续寻找
    #             b=a.xpath('string(.)').extract()
    #             string="".join(b)
    #             if item['keyword'] in string: # 爬取到了有用的正文就可以离开循环
    #                 break
    #             else:
    #                 string="" #否则清空正文字符串 继续循环查找
    #     item['body']=string.replace('\n',"").replace('\t',"").replace(" ","").replace("\r","") # 去除没用的关键字
    #     yield item 