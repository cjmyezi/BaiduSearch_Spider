# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class BaidunewsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    keyword = Field()# 爬取的关键字
    title = Field()# 新闻标题
    brief = Field() # 新闻简介
    body = Field() # 新闻正文
    date = Field() #发文日期
    time = Field() #发文时间
    link = Field() #发文的链接
    platform = Field() # 来源平台或者作者

class BaidusearchSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    keyword = Field()# 爬取的关键字
    number = Field() # 链接序号
    title = Field()# 标题
    time = Field()# 时间
    brief = Field() # 简介内容
    link = Field() # 链接
